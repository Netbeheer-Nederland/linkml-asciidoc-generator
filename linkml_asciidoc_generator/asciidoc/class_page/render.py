from functools import reduce, partial

from linkml_asciidoc_generator.asciidoc import (
    AsciiDocStr,
    Jinja2TemplateStr,
    D2DiagramCodeStr,
    read_jinja2_template,
    CURIE,
    ResourceName,
    PageKind,
    get_page_resource_id,
)
from linkml_asciidoc_generator.linkml.model import LinkMLSchema
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.class_page.model import (
    ClassPage,
    Class,
    PrefixesMap,
    RelationsDiagram,
    Attribute,
    Relation,
)


def _link_curie(curie: CURIE, prefixes: PrefixesMap) -> AsciiDocStr:
    prefix, ncname = curie.split(":")
    base_uri = prefixes[prefix]

    return f"{base_uri}{ncname}[`{curie}`]"


def _xref_resource(name: ResourceName, kind: PageKind) -> AsciiDocStr:
    resource_id = get_page_resource_id(name, kind)

    return f"xref::{resource_id}[`{name}`]"


def _xref_class(class_name: ResourceName) -> AsciiDocStr:
    return _xref_resource(class_name, PageKind.CLASS_PAGE)


def _xref_enum(enum_name: ResourceName) -> AsciiDocStr:
    return _xref_resource(enum_name, PageKind.ENUMERATION_PAGE)


def _xref_slot(
    slot_name: ResourceName,
) -> AsciiDocStr:
    return _xref_resource(slot_name, PageKind.SLOT_PAGE)


def _xref_type(type_name: ResourceName) -> AsciiDocStr:
    return _xref_resource(type_name, PageKind.TYPE_PAGE)


def _render_ancestors(class_: Class) -> AsciiDocStr:
    hierarchy_adoc = reduce(
        lambda acc, succ: f"{acc}{'*'*succ[0]} {_xref_class(succ[1])}\n",
        enumerate(class_.ancestors[::-1], 1),
        "",
    )

    # Self.
    hierarchy_adoc += f"{'*' * (len(class_.ancestors) + 1)} *`{class_.name}`*\n"

    return hierarchy_adoc


def _render_cardinalities(slot: Attribute | Relation):
    return "1..*"
    # if slot.required and slot.multivalued:
    #     return "1..*"
    # elif slot.required and not slot.multivalued:
    #     return "1"
    # elif not slot.required and slot.multivalued:
    #     return "*"
    # else:  # not attr.required and not attr.multivalued
    #     return "0..1"


def _render_relations_diagram(
    diagram: RelationsDiagram, config: Config
) -> D2DiagramCodeStr:
    template = read_jinja2_template(config["templates"]["class_page_relations_diagram"])
    content = template.render(class_=diagram.class_)

    return content


def render_class_page(class_page: ClassPage, config: Config) -> AsciiDocStr:
    template: Jinja2TemplateStr = read_jinja2_template(
        config["templates"]["class_page"]
    )

    if class_page.relations_diagram and len(class_page.class_.relations) > 0:
        relations_diagram: D2DiagramCodeStr = _render_relations_diagram(
            class_page.relations_diagram, config
        )
    else:
        relations_diagram = None

    content = template.render(
        class_=class_page.class_,
        ancestors=_render_ancestors(class_page.class_),
        link_curie=partial(_link_curie, prefixes=class_page.class_.prefixes),
        xref_class=partial(_xref_class),
        xref_enum=partial(_xref_enum),
        xref_slot=partial(_xref_slot),
        xref_type=partial(_xref_type),
        cardinalities=_render_cardinalities,
        relations_diagram=relations_diagram,
    )

    return content
