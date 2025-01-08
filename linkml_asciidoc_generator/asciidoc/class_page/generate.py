from typing import Any
from linkml_asciidoc_generator.linkml.model import (
    LinkMLClass,
    LinkMLSlot,
    LinkMLSlotOwner,
    LinkMLSchema,
    LinkMLPrimitive,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.class_page.model import (
    ClassPage,
    Class,
    Relation,
    Attribute,
    RelationsDiagram,
)
from linkml_asciidoc_generator.linkml.model import SlotDefinition
from linkml_asciidoc_generator.linkml.query import (
    get_ancestors,
    get_relations,
    get_attributes,
)


def _get_min_cardinality(slot: LinkMLSlot) -> Any:
    ...

    min_card = 0

    return min_card


def _get_max_cardinality(slot: LinkMLSlot) -> Any:
    ...

    max_card = "*"

    return max_card


def _generate_data_type(slot_range: Any) -> LinkMLPrimitive:
    ...

    data_type = slot_range

    return data_type


def _generate_attribute(slot_owner: LinkMLSlotOwner, slot: LinkMLSlot) -> Attribute:
    return Attribute(
        name=slot._meta["name"],
        data_type=_generate_data_type(slot.range),
        inherited_from=slot_owner,
        description=slot.description,
        uri=slot.slot_uri,
        min_cardinality=_get_min_cardinality(slot),
        max_cardinalty=_get_max_cardinality(slot),
    )


def _generate_relation(slot_owner: LinkMLSlotOwner, slot: LinkMLSlot) -> Relation:
    return Relation(
        name=slot._meta["name"],
        destination_class=slot.range,
        inherited_from=slot_owner,
        description=slot.description,
        uri=slot.slot_uri,
        min_cardinality=_get_min_cardinality(slot),
        max_cardinalty=_get_max_cardinality(slot),
    )


def _generate_class(class_: LinkMLClass, schema: LinkMLSchema, config: Config) -> Class:
    _class_ = Class(
        name=class_._meta["name"],
        is_abstract=bool(class_.abstract),
        is_mixin=bool(class_.mixin),
        uri=class_.class_uri,
        ancestors=[c._meta["name"] for c in get_ancestors(class_, schema)],
        attributes=[
            _generate_attribute(a[0], a[1]) for a in get_attributes(class_, schema)
        ],
        relations=[
            _generate_relation(r[0], r[1]) for r in get_relations(class_, schema)
        ],
    )

    return _class_


def generate_class_page(
    class_: LinkMLClass, schema: LinkMLSchema, config: Config
) -> ClassPage:
    _class_ = _generate_class(class_, schema, config)

    attributes_diagram = None

    if config["diagrams"]["relations"]:
        relations_diagram = RelationsDiagram(
            name=f"{_class_.name}_relations",
            template=config["templates"]["class_page_relations_diagram"],
            class_=_class_,
        )
    else:
        relations_diagram = None

    page = ClassPage(
        name=_class_.name,
        template=config["templates"]["class_page"],
        title=class_.title or _class_.name,
        class_=_class_,
        relations_diagram=relations_diagram,
        attributes_diagram=attributes_diagram,
    )

    return page


# class RelationsDiagram(MermaidDiagram):
#     class_name: LinkMLClassName

#     return page
#     # relations_diagram: RelationsDiagram | None = None
