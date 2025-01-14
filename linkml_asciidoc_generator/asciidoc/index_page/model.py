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
class IndexPage(Page):
    classes: list[Class]
    enumerations: list[Enumeration]
