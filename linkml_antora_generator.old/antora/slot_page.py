"""
LinkML class -> Antora class page.

"""


# Functions with side effects.
class Config(TypedDict):
    include_relations_diagram: bool
    include_attributes_diagram: bool

def write(class_name: ClassName, schema: SchemaDefinition, tmpl: Jinja2TemplateStr, params: dict) -> None:
    page_adoc = from_linkml_class(class_, schema, tmpl)
    
    # TODO: Write.






def from_linkml_class(class_name: ClassName, schema: SchemaDefinition, tmpl: Jinja2TemplateStr, params: dict) -> AsciiDocStr:
    pass




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
