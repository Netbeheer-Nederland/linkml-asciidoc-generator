from os import PathLike
from . import linkml_full as linkml_type
import yaml

type ClassName = str
type SlotOwnerClassName = str
type Thing = linkml_type.ConfiguredBaseModel


def read(schema_file: PathLike) -> linkml_type.SchemaDefinition:
    schema_dict = _read_file(schema_file)
    schema = init(schema_dict)

    return schema


def _read_file(schema_file: PathLike) -> dict:
    with open(schema_file, mode="rb") as f:
        schema_dict = yaml.safe_load(f)

    return schema_dict


def _set_names(things: dict[Thing]) -> None:
    for name, thing in things.items():
        thing._meta["name"] = name


def init(schema_dict: dict) -> linkml_type.SchemaDefinition:
    schema = linkml_type.SchemaDefinition.model_validate(schema_dict)

    # Set name for elements.
    _set_names(schema.classes or {})
    _set_names(schema.slots or {})
    _set_names(schema.types or {})
    _set_names(schema.enums or {})
    _set_names(schema.subsets or {})

    # Set name for slots and attributes used in classes.
    for class_ in (schema.classes or {}).values():
        _set_names(class_.attributes or {})
        _set_names(class_.slot_usage or {})

    return schema


def get_class(name: ClassName, schema: linkml_type.SchemaDefinition) -> linkml_type.ClassDefinition | None:
    if schema.classes is None or name not in schema.classes:
        return None

    return schema.classes[name]


def get_subclasses(
    class_: linkml_type.ClassDefinition, schema: linkml_type.SchemaDefinition
) -> list[linkml_type.ClassDefinition]:
    return list(filter(lambda c: c.is_a == class_._meta["name"], schema.classes.values()))


def get_superclass(
    class_: linkml_type.ClassDefinition, schema: linkml_type.SchemaDefinition
) -> linkml_type.ClassDefinition | None:
    return get_class(class_.is_a, schema)


def get_ancestors(
    class_: linkml_type.ClassDefinition, schema: linkml_type.SchemaDefinition
) -> list[linkml_type.ClassDefinition]:
    """Superclasses of the given class.

    The list of superclasses is ordered starting with the nearest.
    """

    superclass = get_superclass(class_, schema)

    if superclass is None:
        return []
    else:
        return [superclass] + get_ancestors(superclass, schema)


def is_relation(slot: linkml_type.SlotDefinition, schema: linkml_type.SchemaDefinition) -> bool:
    """Checks whether the given slot is a relationship or not."""

    return slot.range in schema.classes


def is_attribute(slot: linkml_type.SlotDefinition, schema: linkml_type.SchemaDefinition) -> bool:
    """Checks whether the given slot is an attribute."""

    return not is_relation(slot, schema)


def _inherited_slots(
    class_: linkml_type.ClassDefinition, schema: linkml_type.SchemaDefinition
) -> list[tuple[SlotOwnerClassName, linkml_type.SlotDefinition]]:
    slots = []
    for ancestor in get_ancestors(class_, schema):
        if not ancestor.attributes:
            continue

        ancestor_slots = list(ancestor.attributes.values())
        slots.extend((ancestor._meta["name"], ancestor_slot) for ancestor_slot in ancestor_slots)

    return slots


def relations(
    class_: linkml_type.ClassDefinition,
    schema: linkml_type.SchemaDefinition,
    include_inherited: bool = True,
) -> list[tuple[SlotOwnerClassName, linkml_type.SlotDefinition]]:
    # TODO: Expand this so that this also covers `slots` and `slot_usage` (if we allow that one as well).
    class_name = class_._meta["name"]
    _relations = []

    if class_.attributes:
        _relations.extend(zip([class_name] * len(class_.attributes), filter(lambda s: is_relation(s, schema), class_.attributes.values())))

    if include_inherited:
        _relations += list(filter(lambda s: is_relation(s[1], schema), _inherited_slots(class_, schema)))

    # TODO: Filter double _values_ from tuples

    return _relations
    #     _relations = list(filter(lambda s: is_relation(s, schema), class_.attributes.values()))
    #     return list(zip([class_._meta["name"]] * len(_relations), _relations))
    # else:
    #     _relations = list(filter(lambda s: is_relation(s, schema), class_.attributes.values()))
    #     return list(zip([class_._meta["name"]] * len(_relations), _relations))


def attributes(
    class_: linkml_type.ClassDefinition,
    schema: linkml_type.SchemaDefinition,
    include_inherited: bool = True,
) -> list[tuple[SlotOwnerClassName, linkml_type.SlotDefinition]]:
    # TODO: Expand this so that this also covers `slots` and `slot_usage` (if we allow that one as well).
    class_name = class_._meta["name"]
    _attributes = []

    if class_.attributes:
        _attributes.extend(zip([class_name] * len(class_.attributes), filter(lambda s: is_attribute(s, schema), class_.attributes.values())))

    if include_inherited:
        _attributes += list(filter(lambda s: is_attribute(s[1], schema), _inherited_slots(class_, schema)))

    # TODO: Filter double _values_ from tuples

    return _attributes



# def curie(schema, curie, as_curie=True):
#     prefix, local_name = curie.split(":")
#     base_uri = schema.prefixes[prefix]
#     loc = f"{base_uri}{local_name}"

#     if as_curie:
#         return f"{loc}[{prefix}:{local_name}]"
#     else:
#         return f"{loc}[{loc}]"
