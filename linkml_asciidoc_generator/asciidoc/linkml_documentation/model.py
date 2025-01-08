from dataclasses import dataclass

from linkml_asciidoc_generator.asciidoc import Page, ResourceName, AsciiDocStr
from linkml_asciidoc_generator.asciidoc.class_page.model import ClassPage
from linkml_asciidoc_generator.asciidoc.slot_page.model import SlotPage
from linkml_asciidoc_generator.asciidoc.enumeration_page.model import EnumerationPage
from linkml_asciidoc_generator.asciidoc.type_page.model import TypePage


@dataclass
class LinkMLDocumentation:
    name: str
    title: str
    index_page: Page
    navigation_page: Page
    class_pages: dict[ResourceName, ClassPage]
    slot_pages: dict[ResourceName, SlotPage]
    enumeration_pages: dict[ResourceName, EnumerationPage]
    type_pages: dict[ResourceName, TypePage]


@dataclass
class RenderedLinkMLDocumentation:
    name: str
    title: str
    index_page: AsciiDocStr
    navigation_page: AsciiDocStr
    class_pages: dict[ResourceName, AsciiDocStr]
    slot_pages: dict[ResourceName, AsciiDocStr]
    enumeration_pages: dict[ResourceName, AsciiDocStr]
    type_pages: dict[ResourceName, AsciiDocStr]
