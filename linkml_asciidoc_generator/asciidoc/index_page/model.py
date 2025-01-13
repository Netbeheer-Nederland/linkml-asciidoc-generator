from dataclasses import dataclass
from linkml_asciidoc_generator.asciidoc import Page


@dataclass
class Class:
    name: str


@dataclass
class IndexPage(Page):
    classes: list[Class]
