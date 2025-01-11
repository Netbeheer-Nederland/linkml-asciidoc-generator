from dataclasses import dataclass
from linkml_asciidoc_generator.asciidoc import Page
from linkml_asciidoc_generator.linkml.model import LinkMLClass, LinkMLClassName


@dataclass
class NavigationPage(Page):
    classes: dict[LinkMLClassName, LinkMLClass]
    types: list[str]
