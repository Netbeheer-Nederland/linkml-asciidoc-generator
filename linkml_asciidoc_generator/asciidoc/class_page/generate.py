from linkml_asciidoc_generator.linkml.model import (
    LinkMLClass,
    LinkMLEnumeration,
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
    PositiveInt,
)
from linkml_asciidoc_generator.linkml.query import (
    get_ancestors,
    get_descendants,
    get_relations,
    get_attributes,
)
from linkml_asciidoc_generator.asciidoc import (
    get_skos_mappings,
    get_standard_for_class,
    is_cim_data_type,
)


def _get_min_cardinality(slot: LinkMLSlot) -> int:
    match slot.required:
        case False | None:
            return 0
        case True:
            return 1

    return int(slot.required)


def _get_max_cardinality(slot: LinkMLSlot) -> PositiveInt | None:
    match slot.multivalued:
        case False:
            return 1
        case True | None:
            return None


def _generate_data_type(slot_range) -> LinkMLPrimitive | LinkMLEnumeration:
    # `None`
    # TODO: `default_range` should be parsed, then this logic here would probably not be necessary.
    if slot_range is None:
        return LinkMLPrimitive.STRING

    # Primitive
    for enum_val in dict(LinkMLPrimitive.__members__).values():
        if enum_val.value == slot_range:
            return enum_val

    # Enumeration
    return slot_range


def _generate_attribute(slot_owner: LinkMLSlotOwner, slot: LinkMLSlot) -> Attribute:
    return Attribute(
        name=slot._meta["name"],
        data_type=_generate_data_type(slot.range),
        inherited_from=slot_owner,
        description=slot.description,
        uri=slot.slot_uri,
        min_cardinality=_get_min_cardinality(slot),
        max_cardinality=_get_max_cardinality(slot),
        skos_mappings=get_skos_mappings(slot),
        see_also=slot.see_also,
    )


def _generate_relation(
    slot_owner: LinkMLSlotOwner, slot: LinkMLSlot, schema: LinkMLSchema, config: Config
) -> Relation:
    target_class = schema.classes[slot.range]
    return Relation(
        name=slot._meta["name"],
        destination_class=Class(
            name=target_class._meta["name"],
            is_abstract=bool(target_class.abstract),
            is_mixin=bool(target_class.mixin),
            is_cim_data_type=is_cim_data_type(target_class),
            description=target_class.description,
            uri=target_class.class_uri,
            ancestors=[],
            descendants=[],
            attributes=[],
            relations=[],  # No need for these, and can cause recursion errors such as with `Terminal.topologicalNodes <-> TopologicalNode.terminal``
            prefixes=schema.prefixes,
            standard=get_standard_for_class(target_class),
        ),
        inherited_from=slot_owner,
        description=slot.description,
        uri=slot.slot_uri,
        min_cardinality=_get_min_cardinality(slot),
        max_cardinality=_get_max_cardinality(slot),
        skos_mappings=get_skos_mappings(slot),
        see_also=slot.see_also,
    )


def generate_class(class_: LinkMLClass, schema: LinkMLSchema, config: Config) -> Class:
    _class_ = Class(
        name=class_._meta["name"],
        is_abstract=bool(class_.abstract),
        is_mixin=bool(class_.mixin),
        is_root=bool(class_.tree_root),
        is_cim_data_type=is_cim_data_type(class_),
        description=class_.description,
        uri=class_.class_uri,
        ancestors=[c._meta["name"] for c in get_ancestors(class_, schema)],
        descendants=[c._meta["name"] for c in get_descendants(class_, schema)],
        attributes=[
            _generate_attribute(a[0] if a[0] != class_._meta["name"] else None, a[1])
            for a in get_attributes(class_, schema)
        ],
        relations=[
            _generate_relation(
                r[0] if r[0] != class_._meta["name"] else None, r[1], schema, config
            )
            for r in get_relations(class_, schema)
        ],
        prefixes=schema.prefixes,
        standard=get_standard_for_class(class_),
        skos_mappings=get_skos_mappings(class_),
        see_also=class_.see_also,
    )

    return _class_


def generate_class_page(
    class_: LinkMLClass, schema: LinkMLSchema, config: Config
) -> ClassPage:
    _class_ = generate_class(class_, schema, config)

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
    )

    return page
