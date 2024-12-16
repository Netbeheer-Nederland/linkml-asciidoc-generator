from linkml_asciidoc_generator.linkml.model import LinkMLSchema


def _set_names(elements) -> None:
    for name, el in elements.items():
        el._meta["name"] = name


def parse_linkml_schema(schema_dict: dict) -> LinkMLSchema:
    schema = LinkMLSchema.model_validate(schema_dict)

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
