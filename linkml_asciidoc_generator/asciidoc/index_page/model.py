from dataclasses import dataclass
from linkml_asciidoc_generator.asciidoc import Page


@dataclass
class Class:
    name: str
    description: str | None = None


@dataclass
class Enumeration:
    name: str
    description: str | None = None


@dataclass
class CIMDataType:
    name: str
    description: str | None = None


@dataclass
class IndexPage(Page):
    classes: list[Class]
    cim_data_types: list[CIMDataType]
    enumerations: list[Enumeration]
