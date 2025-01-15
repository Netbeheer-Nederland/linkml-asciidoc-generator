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
    xref_type,
    link_curie,
    HexColor,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.class_page.model import (
    ClassPage,
    Class,
    RelationsDiagram,
    Attribute,
    Relation,
    Slot,
)


DEFAULT_COLOR = "#cccccc"


def _render_class_hierarchy(class_: Class) -> AsciiDocStr:
    # Ancestors.
    hierarchy_adoc = reduce(
        lambda acc, succ: f"{acc}{'*' * succ[0]} {xref_class(succ[1])}\n",
        enumerate(class_.ancestors[::-1], 1),
        "",
    )

    # Self.
    depth_self = len(class_.ancestors) + 1
    hierarchy_adoc += f"{'*' * depth_self} *`{class_.name}`*\n"

    # Descendants.
    hierarchy_adoc += reduce(
        lambda acc, succ: f"{acc} {'*' * (depth_self + 1)} {xref_class(succ)}\n",
        sorted(class_.descendants),
        "",
    )

    return hierarchy_adoc


def _render_cardinalities(slot: Attribute | Relation):
    min_cardinality = str(slot.min_cardinality)

    if slot.max_cardinality is None:
        max_cardinality = "*"
    else:
        max_cardinality = str(slot.max_cardinality)

    if min_cardinality == max_cardinality:
        return f"{min_cardinality}"
    else:
        return f"{min_cardinality}..{max_cardinality}"


def _render_relations_diagram(
    diagram: RelationsDiagram, config: Config
) -> D2DiagramCodeStr:
    template = read_jinja2_template(config["templates"]["class_page_relations_diagram"])
    content = template.render(
        class_=diagram.class_,
        color_class=partial(_get_class_color, config=config),
    )

    return content


def _get_class_color(class_: Class, config: Config) -> HexColor:
    try:
        color = config["diagrams"]["class_color"][class_.standard.value]
    except AttributeError:
        color = DEFAULT_COLOR

    return color


def _get_sorted_slots_for_table(slots: list[Slot]) -> list[Slot]:
    def _sort_slots_table(s):
        key = ""
        if s.min_cardinality == 0:
            key += "1"
        else:
            key += "0"

        if s.inherited_from:
            key += "1"
        else:
            key += "0"

        if s.max_cardinality == 1:
            key += "0"
        else:
            key += "1"

        key += s.name
        return key

    slots_for_table = sorted(
        slots,
        key=_sort_slots_table,
    )

    return slots_for_table


def _render_class_page(class_page: ClassPage, config: Config) -> AsciiDocStr:
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
        slots_for_table=_get_sorted_slots_for_table(
            class_page.class_.attributes + class_page.class_.relations
        ),
        class_hierarchy=_render_class_hierarchy(class_page.class_),
        link_curie=partial(link_curie, prefixes=class_page.class_.prefixes),
        xref_class=xref_class,
        xref_enum=xref_enum,
        xref_slot=xref_slot,
        xref_type=xref_type,
        cardinalities=_render_cardinalities,
        relations_diagram=relations_diagram,
    )

    return content


def _get_sorted_slots_for_table_cim_data_type(slots: list[Slot]) -> list[Slot]:
    def _sort_slots_table(s):
        return {"value": 0, "multiplier": 1, "unit": 2}[s.name]

    slots_for_table = sorted(
        slots,
        key=_sort_slots_table,
    )

    return slots_for_table


def _render_cim_data_type_page(class_page: ClassPage, config: Config) -> AsciiDocStr:
    template: Jinja2TemplateStr = read_jinja2_template(
        config["templates"]["cim_data_type_page"]
    )

    content = template.render(
        class_=class_page.class_,
        slots_for_table=_get_sorted_slots_for_table_cim_data_type(
            class_page.class_.attributes + class_page.class_.relations
        ),
        link_curie=partial(link_curie, prefixes=class_page.class_.prefixes),
        xref_class=xref_class,
        xref_enum=xref_enum,
        xref_slot=xref_slot,
        xref_type=xref_type,
        cardinalities=_render_cardinalities,
    )

    return content


def render_class_page(class_page: ClassPage, config: Config) -> AsciiDocStr:
    if class_page.class_.is_cim_data_type:
        return _render_cim_data_type_page(class_page, config)
    else:
        return _render_class_page(class_page, config)
