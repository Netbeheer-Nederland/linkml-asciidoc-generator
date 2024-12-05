from enum import Enum, auto
import jinja2
import subprocess
import textwrap
import os
import os.path
from collections.abc import Callable
import linkml_antora_generator.schema as Schema
from itertools import groupby
from operator import itemgetter
from xml.etree import ElementTree
from urllib.parse import urlparse
from functools import reduce
from pprint import pprint
import shutil
import yaml

from linkml_antora_generator.linkml_full import (
    SchemaDefinition,
    EnumDefinition,
    ClassDefinition,
    SlotDefinition,
)

type ClassName = str
type EnumName = str
type AsciiDocStr = str
type YamlDocStr = str
type AntoraResourceId = str
type AntoraYmlDict = dict  # TODO: Make `TypedDict`.
type MermaidCode = str
type SvgImageStr = str
type CURIE = str


JINJA2_TEMPLATES_DIR = "templates"
ANTORA_COMPONENT_VERSION_DIR = "output"
MERMAID_MMDC = (
    "/home/bart/Programming/Netbeheer-Nederland/docs/node_modules/.bin/mmdc"
)


def default_class_color(class_: ClassDefinition) -> str:
    return "#c1c1c1"


class ResourceType(Enum):
    CLASS_PAGE = auto()
    ENUM_PAGE = auto()
    CLASS_RELATIONS_DIAGRAM = auto()
    NAV_PAGE = auto()


class AntoraGenerator:
    template_map = {ResourceType.CLASS_PAGE: "class.adoc.jinja2", ResourceType.ENUM_PAGE: "enum.adoc.jinja2"}

    def __init__(
        self,
        schemas: set[SchemaDefinition],
        class_color: Callable[[ClassDefinition], str] | None = None,
        output_dir: os.PathLike | None = None,
        metadata: AntoraYmlDict | None = None,
        diagram_background_color: str | None = None,
    ) -> None:
        self.schemas = set(schemas)
        self.class_color = class_color or default_class_color
        self.output_dir = output_dir or ANTORA_COMPONENT_VERSION_DIR
        self.metadata = metadata
        self.diagram_background_color = diagram_background_color or "#ffffff"

        self.jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(JINJA2_TEMPLATES_DIR)
        )

    def _render_template(
        self,
        template_name,
        **kwargs,
    ) -> AsciiDocStr:
        template = self.jinja2_env.get_template(template_name)
        #adoc = template.render(gen=self, **kwargs)
        adoc = template.render(**kwargs)

        return adoc

    def _cardinalities(self, attr):
        if attr.required and attr.multivalued:
            return "1..*"
        elif attr.required and not attr.multivalued:
            return "1"
        elif not attr.required and attr.multivalued:
            return "*"
        else:  # not attr.required and not attr.multivalued
            return "0..1"

    def _resource_id(self, type_, name: str | None = None) -> AntoraResourceId:
        match type_:
            case ResourceType.CLASS_PAGE:
                return f"{name}.adoc"
            case ResourceType.ENUM_PAGE:
                return f"{name}.adoc"
            case ResourceType.CLASS_RELATIONS_DIAGRAM:
                return f"{name}_relations.svg"
            case ResourceType.NAV_PAGE:
                return f"nav.adoc"

    def _class_relations_diagram_mermaid(
        self,
        class_: ClassDefinition,
        relation_slots: list[tuple[str, SlotDefinition]],
    ) -> MermaidCode:
        class_name = class_._meta["name"]
        diagram_code = textwrap.dedent(
            f"""
        %%{{
            init: {{
                'theme': 'base',
                'themeVariables': {{
                'primaryColor': '#CBDCEB',
                'primaryTextColor': '#000000',
                'primaryBorderColor': '#CBDCEB',
                'lineColor': '#000000',
                'secondaryColor': '#006100',
                'tertiaryColor': '#ffffff',
                'fontSize': '12px'
                }}
            }}
        }}%%
        classDiagram
            class {class_name}
        """
        )
        for slot_owner, slot in relation_slots:
            slot_name = slot._meta["name"]
            slot_cardinalities = self._cardinalities(slot)
            diagram_code += f'\t{class_name} --> "{slot_cardinalities}" {slot.range}: {slot_name}\n'
        return diagram_code

    def class_relations_diagram(self, schema: SchemaDefinition, class_: ClassDefinition) -> SvgImageStr:
        class_name = class_._meta["name"]
        relation_slots = Schema.relations(class_, schema)
        diagram_res_id = self._resource_id(
            ResourceType.CLASS_RELATIONS_DIAGRAM, class_name
        )
        diagram_name = diagram_res_id.split(".svg")[0]

        diagram_code = self._class_relations_diagram_mermaid(
            class_, relation_slots
        )

        diagram_svg = self._mermaid_to_svg(diagram_code, diagram_name)

        colored_diagram_svg = self._colored_class_relations_diagram(
            diagram_svg,
            diagram_name,
        )

        return colored_diagram_svg

    def _colored_class_relations_diagram(
        self,
        schema: SchemaDefinition,
        diagram_svg: SvgImageStr,
        diagram_name: str,
    ) -> SvgImageStr:
        svg_ns = "http://www.w3.org/2000/svg"
        html_ns = "http://www.w3.org/1999/xhtml"
        svg_root = ElementTree.fromstring(diagram_svg)

        # Set label background.
        style = svg_root.find(f"{{{svg_ns}}}style")
        style.text += f"#{diagram_name} .edgeLabel .label span {{background: {self.diagram_background_color};}}"

        # Set class colors.
        for class_node in svg_root.findall(
            ".//svg:g[@class='nodes']/svg:g",
            namespaces={"svg": "http://www.w3.org/2000/svg"},
        ):
            class_label = class_node.findtext(
                f".//{{{html_ns}}}span/{{{html_ns}}}p"
            )
            try:
                color = self.class_color(schema.classes[class_label])
            except KeyError:
                color = "#cccccc"

            for path in class_node.findall(f".//{{{svg_ns}}}path"):
                path.attrib["style"] = f"fill: {color}; stroke: {color}"

        colored_diagram_svg = ElementTree.tostring(svg_root)

        return colored_diagram_svg


    def _enum_page(self, enum: EnumDefinition) -> AsciiDocStr:
        enum_name = enum._meta["name"]

        return self._render_template(
            self.template_map[ResourceType.ENUM_PAGE],
            enum=enum,
            enum_name=enum_name,
            enum_xref=self._enum_xref,
            link_curie=self._link_curie,
        )


    def _class_hierarchy(self, class_: ClassDefinition) -> AsciiDocStr:
        return self._class_ancestors(class_) + self._class_descendants(class_)


    def _class_ancestors(self, schema: SchemaDefinition, class_: ClassDefinition) -> AsciiDocStr:
        # Ancestors.
        ancestor_classes = [
            c._meta["name"] for c in Schema.get_ancestors(class_, schema)
        ][::-1]
        hierarchy_adoc = reduce(
            lambda acc, succ: f"{acc}{'*'*succ[0]} {self._class_xref(succ[1])}\n",
            enumerate(ancestor_classes, 1),
            "",
        )

        # Self.
        hierarchy_adoc += (
            f"{'*' * (len(ancestor_classes) + 1)} *`{class_._meta['name']}`*\n"
        )

        return hierarchy_adoc

    def _class_descendants(self, schema: SchemaDefinition, class_: ClassDefinition) -> AsciiDocStr:
        # Descendants.

        subclasses = sorted(
            [
                c._meta["name"]
                for c in Schema.get_subclasses(class_, schema)
            ]
        )[:3]
        hierarchy_adoc = reduce(
            lambda acc, succ: f"{acc} * {self._class_xref(succ)}\n",
            subclasses,
            "",
        )

        return hierarchy_adoc

    def _class_xref(self, class_name: ClassName, mono: bool = True) -> AsciiDocStr:
        class_res_id = self._resource_id(ResourceType.CLASS_PAGE, class_name)
        return f"xref::{class_res_id}[`{class_name}`]"


    def _enum_xref(self, enum_name: EnumName) -> AsciiDocStr:
        enum_res_id = self._resource_id(ResourceType.ENUM_PAGE, enum_name)
        return f"xref::{enum_res_id}[`{enum_name}`]"


    def _link_curie(self, schema: SchemaDefinition, curie: CURIE) -> AsciiDocStr:
        prefix, ncname = curie.split(":")
        base_uri = schema.prefixes[prefix]
        return f"{base_uri}{ncname}[`{curie}`]"


    def _class_page(
        self,
        schema: SchemaDefinition,
        class_: ClassDefinition,
        relations_diagram_res_id: AntoraResourceId | None,
    ) -> AsciiDocStr:
        class_name = class_._meta["name"]

        return self._render_template(
            self.template_map[ResourceType.CLASS_PAGE],
            class_=class_,
            class_name=class_name,
            class_type=self.class_type(class_),
            class_hierarchy=self._class_hierarchy(class_),
            relations=Schema.relations(class_, schema),
            render_images=True,
            attributes=Schema.attributes(class_, schema),
            cardinalities=self._cardinalities,
            class_xref=self._class_xref,
            link_curie=self._link_curie,
            class_relations_diagram_res_id=relations_diagram_res_id,
            class_attributes_diagram_res_id=relations_diagram_res_id,
        )

    def class_type(self, class_: ClassDefinition):
        if class_.abstract and class_.mixin:
            return "Abstract mixin class"
        elif class_.abstract:
            return "Abstract class"
        elif class_.mixin:
            return "Mixin class"
        else:
            return "Class"

    def _mermaid_to_svg(self, code: str, name: str) -> SvgImageStr:
        result = subprocess.run(
            [
                MERMAID_MMDC,
                "--theme",
                "neutral",
                "--outputFormat",
                "svg",
                "--svgId",
                name,
                "--output",
                "-",
            ],
            input=code.encode("utf-8"),
            capture_output=True,
        )
        assert result.returncode == 0
        svg_image = result.stdout

        return svg_image

    def _write_file(
            self, schema: SchemaDefinition, content: bytes, resource_id: AntoraResourceId
    ) -> os.PathLike:
        # TODO: Improve.
        if resource_id.endswith(".svg"):
            family = "images"
        elif resource_id == "nav.adoc":
            family = ""
        else:
            family = "pages"

        filepath = os.path.join(self.output_dir, schema.id, family, resource_id)
        with open(filepath, mode="wb") as f:
            f.write(content)

        return filepath

    def _nav_page(self, schema: SchemaDefinition) -> AsciiDocStr:
        nav = ".Classes\n"
        for section_letter, classes_group in groupby(sorted(schema.classes), key=itemgetter(0)):
            nav += f"* {section_letter}\n"
            for class_ in classes_group:
                nav += f"** {self._class_xref(class_, mono=False)}\n"

        nav += ".Enumerations\n"
        for enum in schema.enums:
            nav += f"* {self._enum_xref(enum)}\n"

        #nav = reduce(
        #    lambda acc, succ: f"{acc}* {self._class_xref(succ)}\n",
        #schema.classes.keys(),
        #"",
        #)
        return nav

    def _component_version_descriptor(self, metadata: AntoraYmlDict) -> YamlDocStr:
        if "version" not in metadata:
            metadata["version"] = True

        antora_yml = yaml.safe_dump(antora_yml_dict)

        return antora_yml

    # ~~~ Methods with side effects.

    def _create_component_version_descriptor(self) -> os.PathLike:
        antora_yml = self._component_version_descriptor(self.metadata)
        self._write_file(antora_yml.encode("utf-8"))  # TODO


    def _create_nav_page(self) -> None:
        nav_page: AsciiDocStr = self._nav_page()
        nav_res_id = self._resource_id(ResourceType.NAV_PAGE)
        self._write_file(nav_page.encode("utf-8"), nav_res_id)

    def _create_enum_page(self, schema: SchemaDefinition, enum_name: EnumName) -> None:
        enum = schema.enums[enum_name]

        enum_page: AsciiDocStr = self._enum_page(enum)
        enum_res_id = self._resource_id(ResourceType.ENUM_PAGE, enum_name)
        self._write_file(enum_page.encode("utf-8"), enum_res_id)

    def _create_class_page(self, schema: SchemaDefinition, class_name: ClassName, incl_relations_diagram: bool = False) -> None:
        class_= schema.classes[class_name]

        relation_slots = Schema.relations(class_, schema)

        relations_diagram_res_id = None
        if relation_slots:
            relations_diagram: SvgImageStr = self.class_relations_diagram(
                class_
            )
            relations_diagram_res_id = self._resource_id(
                ResourceType.CLASS_RELATIONS_DIAGRAM, class_name
            )
            self._write_file(relations_diagram, relations_diagram_res_id)

        class_page: AsciiDocStr = self._class_page(
            class_, relations_diagram_res_id
        )
        class_res_id = self._resource_id(ResourceType.CLASS_PAGE, class_name)
        self._write_file(class_page.encode("utf-8"), class_res_id)

    def _module_dir(self, name: str) -> os.PathLike:
        return os.path.join(self.output_dir, "modules", name)

    def _create_module_dir(self, name: str) -> os.PathLike:
        dir_path = self._module_dir(name)
        os.makedirs(dir_path, exist_ok=True)

        return dir_path

    def _create_module(self, schema: SchemaDefinition, name: str | None = None) -> None:
        if not name:
            name = schema.id

        module_dir = self._create_module_dir(name)

        for class_name in schema.classes:
            self._create_class_page(schema, class_name)

        for enum_name in schema.enums:
            self._create_enum_page(schema, enum_name)

        #for type_name in schema.types:
        #    self._create_type_page(schema, enum_name)

        self._create_nav_page()

    def _create_output_dir(self) -> None:
        os.makedirs(self.output_dir, exist_ok=True)

    def _clean_output_dir(self) -> None:
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def _init_output_dir(self) -> None:
        self._clean_output_dir()
        self._create_output_dir()

    def _create_component_version(self) -> None:
        self._init_output_dir()
        self._create_component_version_descriptor()

        if len(self.schemas) == 1:
            self._create_module(self.schemas[0], name="ROOT")
        else:
            for schema in self.schemas:
                self._create_module(schema)

    def create_docs(self) -> None:
        """Entry point.
        """

        self._create_component_version()
