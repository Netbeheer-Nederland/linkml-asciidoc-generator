from linkml_asciidoc_generator.model.linkml import (
    LinkMLClass,
    LinkMLSchema,
    LinkMLSlot,
    LinkMLClassName,
    LinkMLSlotOwner,
)


def get_class(name: LinkMLClassName, schema: LinkMLSchema) -> LinkMLClass | None:
    if schema.classes is None or name not in schema.classes:
        return None

    return schema.classes[name]


def get_superclass(class_: LinkMLClass, schema: LinkMLSchema) -> LinkMLClass | None:
    return get_class(class_.is_a, schema)


def get_descendants(class_: LinkMLClass, schema: LinkMLSchema) -> list[LinkMLClass]:
    return list(
        filter(lambda c: c.is_a == class_._meta["name"], schema.classes.values())
    )


def get_ancestors(class_: LinkMLClass, schema: LinkMLSchema) -> list[LinkMLClass]:
    """Superclasses of the given class.

    The list of superclasses is ordered starting with the nearest.
    """

    superclass = get_superclass(class_, schema)

    if superclass is None:
        return []
    else:
        return [superclass] + get_ancestors(superclass, schema)


def is_relation(slot: LinkMLSlot, schema: LinkMLSchema) -> bool:
    """Checks whether the given slot is a relationship or not."""

    return slot.range in schema.classes


def is_attribute(slot: LinkMLSlot, schema: LinkMLSchema) -> bool:
    """Checks whether the given slot is an attribute."""

    return not is_relation(slot, schema)


def get_inherited_slots(
    class_: LinkMLClass, schema: LinkMLSchema
) -> dict[LinkMLSlotOwner, LinkMLSlot]:
    slots = []
    for ancestor in get_ancestors(class_, schema):
        if not ancestor.attributes:
            continue

        ancestor_slots = list(ancestor.attributes.values())
        slots.extend(
            (ancestor._meta["name"], ancestor_slot) for ancestor_slot in ancestor_slots
        )

    return slots


def get_relations(
    class_: LinkMLClass,
    schema: LinkMLSchema,
    include_inherited: bool = True,
) -> dict[LinkMLSlotOwner, LinkMLSlot]:
    # TODO: Expand this so that this also covers `slots` and `slot_usage` (if we allow that one as well).
    class_name = class_._meta["name"]
    _relations = []

    if class_.attributes:
        _relations.extend(
            zip(
                [class_name] * len(class_.attributes),
                filter(lambda s: is_relation(s, schema), class_.attributes.values()),
            )
        )

    if include_inherited:
        _relations += list(
            filter(
                lambda s: is_relation(s[1], schema),
                get_inherited_slots(class_, schema),
            )
        )

    # TODO: Filter double _values_ from tuples

    return _relations


def get_attributes(
    class_: LinkMLClass,
    schema: LinkMLSchema,
    include_inherited: bool = True,
) -> dict[LinkMLSlotOwner, LinkMLSlot]:
    # TODO: Expand this so that this also covers `slots` and `slot_usage` (if we allow that one as well).
    class_name = class_._meta["name"]
    _attributes = []

    if class_.attributes:
        _attributes.extend(
            zip(
                [class_name] * len(class_.attributes),
                filter(lambda s: is_attribute(s, schema), class_.attributes.values()),
            )
        )

    if include_inherited:
        _attributes += list(
            filter(
                lambda s: is_attribute(s[1], schema),
                get_inherited_slots(class_, schema),
            )
        )

    # TODO: Filter double _values_ from tuples

    return _attributes
