import os
import os.path

from typing import IO

from linkml_asciidoc_generator.asciidoc.linkml_documentation.model import (
    RenderedLinkMLDocumentation,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc import (
    ResourceName,
    PageKind,
    get_page_resource_id,
)


def _write_page(
    name: ResourceName, kind: PageKind, content: IO, config: Config
) -> None:
    page_resource_id = get_page_resource_id(name, kind, config)
    page_dir, page_filename = os.path.split(page_resource_id)

    os.makedirs(page_dir, exist_ok=True)

    with open(page_resource_id, mode="wb") as f:
        f.write(content.encode(config["char_encoding"]))


def write_linkml_documentation(
    linkml_documentation: RenderedLinkMLDocumentation, config: Config
) -> None:
    _write_page("index", PageKind.INDEX_PAGE, linkml_documentation.index_page, config)
    _write_page(
        "nav",
        PageKind.NAVIGATION_PAGE,
        linkml_documentation.navigation_page,
        config,
    )

    for name, content in linkml_documentation.class_pages.items():
        if content is not None:
            _write_page(name, PageKind.CLASS_PAGE, content, config)

    for name, content in linkml_documentation.slot_pages.items():
        if content is not None:
            _write_page(name, PageKind.SLOT_PAGE, content, config)

    for name, content in linkml_documentation.enumeration_pages.items():
        if content is not None:
            _write_page(name, PageKind.ENUMERATION_PAGE, content, config)

    for name, content in linkml_documentation.type_pages.items():
        if content is not None:
            _write_page(name, PageKind.TYPE_PAGE, content, config)
