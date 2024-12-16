from typing import NamedTuple

from linkml_asciidoc_generator.asciidoc.model import Page
from linkml_asciidoc_generator.asciidoc.model.class_page import ClassPage
from linkml_asciidoc_generator.asciidoc.model.slot_page import SlotPage
from linkml_asciidoc_generator.asciidoc.model.enumeration_page import EnumerationPage
from linkml_asciidoc_generator.asciidoc.model.type_page import TypePage


class LinkMLDocumentation(NamedTuple):
    name: str
    index_page: Page
    navigation_page: Page
    class_pages: frozenset[ClassPage]
    slot_pages: frozenset[SlotPage]
    enumeration_pages: frozenset[EnumerationPage]
    type_pages: frozenset[TypePage]
