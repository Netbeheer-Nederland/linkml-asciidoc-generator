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
    generate_used_by,
)


def _generate_enumeration_value(
    enum: LinkMLEnumeration, pv_name: str
) -> EnumerationValue:
    pv: LinkMLEnumerationValue = enum.permissible_values[pv_name]
    enumeration_value = EnumerationValue(description=pv.description,
                                         value=pv_name, uri=pv.meaning)

    return enumeration_value


def generate_enumeration(enum: LinkMLEnumeration, schema: LinkMLSchema) -> Enumeration:
    enumeration = Enumeration(
        name=enum._meta["name"],
        description=enum.description,
        uri=enum.enum_uri,
        used_by=generate_used_by(enum, schema),
        values=[
            _generate_enumeration_value(enum, pv_name)
            for pv_name in (
                enum.permissible_values or []
            )  # TODO: This should be taken care of more thoroughly in the data model.
        ],
        prefixes=schema.prefixes,
        standard=get_standard_for_enumeration(enum),
        skos_mappings=get_skos_mappings(enum),
        see_also=enum.see_also,
    )

    return enumeration


def generate_enumeration_page(
    enum: LinkMLEnumeration, schema: LinkMLSchema, config: Config
) -> EnumerationPage:
    enumeration = generate_enumeration(enum, schema)

    enumeration_page = EnumerationPage(
        name=enumeration.name,
        enumeration=enumeration,
        template=config["templates"]["enumeration_page"],
        title=enum.title or enumeration.name,
    )

    return enumeration_page
