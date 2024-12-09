"""
LinkMLSchema -> AntoraModule
"""

from linkml_antora_generator.linkml.types import *
from linkml_antora_generator.antora.types import *
from linkml_antora_generator.antora.class_page import generate_class_page
from linkml_antora_generator.antora.slot_page import generate_slot_page
from linkml_antora_generator.antora.enumeration_page import generate_enumeration_page
from linkml_antora_generator.antora.type_page import generate_type_page


def _module_name(name: str) -> str:
    return name.replace("-", "_")


def _resource_id(kind, name: str | None = None) -> AntoraResourceID:
    match kind:
        case AntoraResourceKind.CLASS_PAGE:
            return f"{name}.adoc"
        case AntoraResourceKind.ENUM_PAGE:
            return f"{name}.adoc"
        case AntoraResourceKind.CLASS_RELATIONS_DIAGRAM:
            return f"{name}_relations.svg"
        case AntoraResourceKind.NAV_PAGE:
            return f"nav.adoc"


def generate_module(schema: LinkMLSchema, config: AntoraConfig | None = None) -> AntoraModule:
    module_name = _module_name(config.module_name or schema.name)

    class_pages = {_resource_id(c): generate_class_page(c, schema=schema, config=config) for c in schema.classes}
    slot_pages = {s._meta["name"]: generate_slot_page(s, schema=schema, config=config) for s in schema.slots}
    enumeration_pages = {
        e._meta["name"]: generate_enumeration_page(e, schema=schema, config=config) for e in schema.enums
    }
    type_pages = {t._meta["name"]: generate_type_page(t, schema=schema, config=config) for t in schema.types}

    return AntoraModule(
        name=module_name,
        pages=class_pages | slot_pages | enumeration_pages | type_pages,
        images=images,
        attachments={},
        examples={},
        partials={},
    )
