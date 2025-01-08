import os
import os.path

from typing import IO

from linkml_asciidoc_generator.asciidoc.linkml_documentation.model import (
    RenderedLinkMLDocumentation,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc import Page, ResourceName, ResourceKind
from linkml_asciidoc_generator.asciidoc.class_page.model import ClassPage
from linkml_asciidoc_generator.asciidoc.slot_page.model import SlotPage
from linkml_asciidoc_generator.asciidoc.enumeration_page.model import EnumerationPage
from linkml_asciidoc_generator.asciidoc.type_page.model import TypePage
from linkml_asciidoc_generator.asciidoc.index_page.model import IndexPage
from linkml_asciidoc_generator.asciidoc.navigation_page.model import NavigationPage


def _write_page(
    name: ResourceName, kind: ResourceKind, content: IO, config: Config
) -> None:
    match kind:
        case ResourceKind.CLASS_PAGE:
            page_type = "class"
        case ResourceKind.SLOT_PAGE:
            page_type = "slot"
        case ResourceKind.ENUMERATION_PAGE:
            page_type = "enumeration"
        case ResourceKind.TYPE_PAGE:
            page_type = "type"
        case ResourceKind.INDEX_PAGE:
            page_type = ""
        case ResourceKind.NAVIGATION_PAGE:
            page_type = ""
        case _:
            page_type = ""

    page_dir = os.path.join(config["output_dir"], page_type)
    page_filename = f"{name}.adoc"

    os.makedirs(page_dir, exist_ok=True)

    with open(os.path.join(page_dir, page_filename), mode="wb") as f:
        f.write(content.encode(config["char_encoding"]))


def write_linkml_documentation(
    linkml_documentation: RenderedLinkMLDocumentation, config: Config
) -> None:
    _write_page(
        "index", ResourceKind.INDEX_PAGE, linkml_documentation.index_page, config
    )
    _write_page(
        "nav",
        ResourceKind.NAVIGATION_PAGE,
        linkml_documentation.navigation_page,
        config,
    )

    for name, content in linkml_documentation.class_pages.items():
        if content is not None:
            _write_page(name, ResourceKind.CLASS_PAGE, content, config)

    for name, content in linkml_documentation.slot_pages.items():
        if content is not None:
            _write_page(name, ResourceKind.SLOT_PAGE, content, config)

    for name, content in linkml_documentation.enumeration_pages.items():
        if content is not None:
            _write_page(name, ResourceKind.ENUMERATION_PAGE, content, config)

    for name, content in linkml_documentation.type_pages.items():
        if content is not None:
            _write_page(name, ResourceKind.TYPE_PAGE, content, config)
