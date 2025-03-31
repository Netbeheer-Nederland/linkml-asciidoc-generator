from dataclasses import dataclass
from linkml_asciidoc_generator.asciidoc import (
    Page,
    PrefixesMap,
    CURIE,
    URI,
    CIMStandard,
    SkosMapping,
    UsedByMap,
)
from linkml_asciidoc_generator.linkml.model import LinkMLElementName


@dataclass
class EnumerationValue:
    value: str
    uri: CURIE


@dataclass
class Enumeration:
    name: LinkMLElementName
    values: list[EnumerationValue]
    prefixes: PrefixesMap
    uri: CURIE | None = None
    standard: CIMStandard | None = None
    description: str | None = None
    used_by: UsedByMap | None = None
    skos_mappings: SkosMapping | None = None
    see_also: list[URI] | None = None


@dataclass
class EnumerationPage(Page):
    enumeration: Enumeration
