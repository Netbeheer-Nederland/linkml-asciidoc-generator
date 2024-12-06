"""
LinkMLSchema -> AntoraModule
"""

from linkml_antora_generator.linkml.types import *
from linkml_antora_generator.antora.types import *


def generate_module(schema: LinkMLSchema, name: str | None = None, config: AntoraConfig | None = None) -> AntoraModule:
    if not name:
        name = schema.name.replace("-", "_")

    class_pages = (generate_class_page(class_, schema=schema, config=config) for class_ in schema.classes)
    enumeration_pages = (generate_enumeration_page(class_, schema=schema, config=config) for class_ in schema.enums)
    type_pages = (generate_type_page(class_, schema=schema, config=config) for class_ in schema.types)
    # TODO: Out of scope for now:
    # slot_pages = {generate_slot_page(class_, schema=schema, config=config) for class_ in schema.classes}

    images = set()

    # TODO: Out of scope for now:
    # if config.include_attributes_diagram:
    #     pass

    return AntoraModule(
        name=name,
        pages=class_pages | enumeration_pages | type_pages,
        images=images,
        # TODO: Out of scope for now:
        # attachments=attachments,
        # examples=examples,
        # partials=partials,
    )
