import os
import os.path

from linkml_asciidoc_generator.asciidoc.linkml_documentation.model import (
    RenderedLinkMLDocumentation,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc import Page
from linkml_asciidoc_generator.asciidoc.class_page.model import ClassPage
from linkml_asciidoc_generator.asciidoc.slot_page.model import SlotPage
from linkml_asciidoc_generator.asciidoc.enumeration_page.model import EnumerationPage
from linkml_asciidoc_generator.asciidoc.type_page.model import TypePage
from linkml_asciidoc_generator.asciidoc.index_page.model import IndexPage
from linkml_asciidoc_generator.asciidoc.navigation_page.model import NavigationPage


def _write_page(page: Page, config: Config) -> None:
    match page:
        case ClassPage():
            page_type = "class"
        case SlotPage():
            page_type = "slot"
        case EnumerationPage():
            page_type = "enumeration"
        case TypePage():
            page_type = "type"
        case IndexPage():
            page_type = ""
        case NavigationPage():
            page_type = ""
        case _:
            page_type = ""

    page_dir = os.path.join(config["output_dir"], page_type)
    page_filename = f"{page.name}.adoc"

    os.makedirs(page_dir, exist_ok=True)

    with open(os.path.join(page_dir, page_filename), mode="w") as f:
        f.write(page.content)


def write_linkml_documentation_project(
    linkml_documentation_project: RenderedLinkMLDocumentation, config: Config
) -> None:
    for class_page in linkml_documentation_project.class_pages:
        _write_page(class_page, config)

    for slot_page in linkml_documentation_project.slot_pages:
        _write_page(slot_page, config)

    for enumeration_page in linkml_documentation_project.enumeration_pages:
        _write_page(enumeration_page, config)

    for type_page in linkml_documentation_project.type_pages:
        _write_page(type_page, config)
