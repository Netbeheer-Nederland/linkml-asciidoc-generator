from linkml_asciidoc_generator.linkml.model import (
    LinkMLEnumeration,
    LinkMLEnumerationValue,
    LinkMLSchema,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.enumeration_page.model import (
    EnumerationPage,
    Enumeration,
    EnumerationValue,
)
from linkml_asciidoc_generator.asciidoc import (
    get_standard_for_enumeration,
    get_skos_mappings,
)


def _generate_enumeration_value(
    enum: LinkMLEnumeration, pv_name: str
) -> EnumerationValue:
    pv: LinkMLEnumerationValue = enum.permissible_values[pv_name]
    enumeration_value = EnumerationValue(value=pv_name, uri=pv.meaning)

    return enumeration_value


def _generate_enumeration(enum: LinkMLEnumeration, schema: LinkMLSchema) -> Enumeration:
    enumeration = Enumeration(
        name=enum._meta["name"],
        description=enum.description,
        uri=enum.enum_uri,
        values=[
            _generate_enumeration_value(enum, pv_name)
            for pv_name in enum.permissible_values
        ],
        prefixes=schema.prefixes,
        standard=get_standard_for_enumeration(enum),
        skos_mappings=get_skos_mappings(enum),
    )

    return enumeration


def generate_enumeration_page(
    enum: LinkMLEnumeration, schema: LinkMLSchema, config: Config
) -> EnumerationPage:
    enumeration = _generate_enumeration(enum, schema)

    enumeration_page = EnumerationPage(
        name=enumeration.name,
        enumeration=enumeration,
        template=config["templates"]["enumeration_page"],
        title=enum.title or enumeration.name,
    )

    return enumeration_page
