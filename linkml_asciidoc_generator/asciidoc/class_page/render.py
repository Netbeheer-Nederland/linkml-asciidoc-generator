from functools import reduce, partial

from linkml_asciidoc_generator.asciidoc import (
    AsciiDocStr,
    Jinja2TemplateStr,
    D2DiagramCodeStr,
    read_jinja2_template,
    xref_class,
    xref_enum,
    xref_slot,
    xref_type,
    link_curie,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.class_page.model import (
    ClassPage,
    Class,
    RelationsDiagram,
    Attribute,
    Relation,
)


def _render_ancestors(class_: Class) -> AsciiDocStr:
    hierarchy_adoc = reduce(
        lambda acc, succ: f"{acc}{'*'*succ[0]} {xref_class(succ[1])}\n",
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
        link_curie=partial(link_curie, prefixes=class_page.class_.prefixes),
        xref_class=xref_class,
        xref_enum=xref_enum,
        xref_slot=xref_slot,
        xref_type=xref_type,
        cardinalities=_render_cardinalities,
        relations_diagram=relations_diagram,
    )

    return content
