import os
import os.path

from typing import IO
from os import PathLike

from linkml_asciidoc_generator.asciidoc.linkml_documentation.model import (
    RenderedLinkMLDocumentation,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc import (
    PageKind,
    get_page_resource_id,
    CharEncoding,
)


def _write_page(content: IO, file_path: PathLike, char_encoding: CharEncoding) -> None:
    page_dir, page_filename = os.path.split(file_path)

    os.makedirs(page_dir, exist_ok=True)

    with open(file_path, mode="wb") as f:
        f.write(content.encode(char_encoding))


def write_linkml_documentation(
    linkml_documentation: RenderedLinkMLDocumentation, config: Config
) -> None:
    """Writes the content to files on disk.

    Currently, the output is structured as an Antora module for use in
    an Antora component version.
    """

    # module_dir = os.path.join(config["output_dir"], linkml_documentation.name.lower())
    module_dir = config["output_dir"]

    pages_dir = os.path.join(module_dir, "pages")
    partials_dir = os.path.join(module_dir, "partials")
    images_dir = os.path.join(module_dir, "images")
    attachments_dir = os.path.join(module_dir, "attachments")
    examples_dir = os.path.join(module_dir, "examples")

    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(partials_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(attachments_dir, exist_ok=True)
    os.makedirs(examples_dir, exist_ok=True)

    index_page_path = os.path.join(
        pages_dir,
        get_page_resource_id("index", PageKind.INDEX_PAGE),
    )
    _write_page(
        linkml_documentation.index_page, index_page_path, config["char_encoding"]
    )

    navigation_page_path = os.path.join(
        module_dir,
        get_page_resource_id("nav", PageKind.NAVIGATION_PAGE),
    )
    _write_page(
        linkml_documentation.navigation_page,
        navigation_page_path,
        config["char_encoding"],
    )

    for name, content in linkml_documentation.class_pages.items():
        if content is not None:
            class_page_path = os.path.join(
                pages_dir,
                get_page_resource_id(name, PageKind.CLASS_PAGE),
            )
            _write_page(content, class_page_path, config["char_encoding"])

    for name, content in linkml_documentation.slot_pages.items():
        if content is not None:
            slot_page_path = os.path.join(
                pages_dir,
                get_page_resource_id(name, PageKind.SLOT_PAGE),
            )
            _write_page(content, slot_page_path, config["char_encoding"])

    for name, content in linkml_documentation.enumeration_pages.items():
        if content is not None:
            enumeration_page_path = os.path.join(
                pages_dir,
                get_page_resource_id(name, PageKind.ENUMERATION_PAGE),
            )
            _write_page(content, enumeration_page_path, config["char_encoding"])

    for name, content in linkml_documentation.type_pages.items():
        if content is not None:
            type_page_path = os.path.join(
                pages_dir,
                get_page_resource_id(name, PageKind.TYPE_PAGE),
            )
            _write_page(content, type_page_path, config["char_encoding"])
