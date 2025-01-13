from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.linkml_documentation.model import (
    LinkMLDocumentation,
    RenderedLinkMLDocumentation,
)
from linkml_asciidoc_generator.asciidoc.index_page.render import (
    render_index_page,
)
from linkml_asciidoc_generator.asciidoc.navigation_page.render import (
    render_navigation_page,
)
from linkml_asciidoc_generator.asciidoc.class_page.render import render_class_page
from linkml_asciidoc_generator.asciidoc.slot_page.render import render_slot_page
from linkml_asciidoc_generator.asciidoc.enumeration_page.render import (
    render_enumeration_page,
)
from linkml_asciidoc_generator.asciidoc.type_page.render import render_type_page


def render_linkml_documentation(
    linkml_documentation: LinkMLDocumentation, config: Config
) -> RenderedLinkMLDocumentation:
    linkml_documentation = LinkMLDocumentation(
        name=linkml_documentation.name,
        title=linkml_documentation.title,
        index_page=render_index_page(linkml_documentation.index_page, config),
        navigation_page=render_navigation_page(
            linkml_documentation.navigation_page, config
        ),
        class_pages={
            name: render_class_page(page, config)
            for name, page in linkml_documentation.class_pages.items()
        },
        slot_pages={
            name: render_slot_page(page, config)
            for name, page in linkml_documentation.slot_pages.items()
        },
        enumeration_pages={
            name: render_enumeration_page(page, config)
            for name, page in linkml_documentation.enumeration_pages.items()
        },
        type_pages={
            name: render_type_page(page, config)
            for name, page in linkml_documentation.type_pages.items()
        },
    )

    return linkml_documentation
