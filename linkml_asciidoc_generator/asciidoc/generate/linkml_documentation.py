from linkml_asciidoc_generator.linkml.model import LinkMLSchema
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.model import Page
from linkml_asciidoc_generator.asciidoc.model.linkml_documentation import (
    LinkMLDocumentation,
)
from linkml_asciidoc_generator.asciidoc.generate.helper.template import (
    read_jinja2_template,
)
from linkml_asciidoc_generator.asciidoc.generate.class_page import generate_class_page


def _generate_index_page(schema: LinkMLSchema) -> Page:
    # TODO:
    # - Implement
    # - Move to own module?
    index_page = None

    return index_page


def _generate_navigation_page(schema: LinkMLSchema) -> Page:
    # TODO:
    # - Implement
    # - Move to own module?
    navigation_page = None

    return navigation_page


def generate_linkml_documentation(
    schema: LinkMLSchema, config: Config
) -> LinkMLDocumentation:
    index_page = _generate_index_page(schema)
    navigation_page = _generate_navigation_page(schema)

    linkml_documentation = LinkMLDocumentation(
        name=schema.name,
        title=schema.title or schema.name,
        index_page=index_page,
        navigation_page=navigation_page,
        class_pages=class_pages,
        slot_pages=slot_pages,
        enumeration_pages=enumeration_pages,
        type_pages=type_pages,
    )
    return linkml_documentation
