from linkml_asciidoc_generator.linkml.model import LinkMLSchema
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.linkml_documentation.model import (
    LinkMLDocumentation,
)
from linkml_asciidoc_generator.asciidoc.class_page.generate import generate_class_page
from linkml_asciidoc_generator.asciidoc.enumeration_page.generate import (
    generate_enumeration_page,
)
from linkml_asciidoc_generator.asciidoc.index_page.generate import generate_index_page
from linkml_asciidoc_generator.asciidoc.navigation_page.generate import (
    generate_navigation_page,
)


def generate_linkml_documentation(
    schema: LinkMLSchema, config: Config
) -> LinkMLDocumentation:
    index_page = generate_index_page(schema, config)
    navigation_page = generate_navigation_page(schema, config)

    class_pages = {
        c._meta["name"]: generate_class_page(c, schema, config)
        for c in schema.classes.values()
        if c._meta["name"]
        # in ["MarketEvaluationPoint", "UsagePoint", "Substation", "ActivePower"]
    }

    slot_pages = {}
    enumeration_pages = {
        e._meta["name"]: generate_enumeration_page(e, schema, config)
        for e in schema.enums.values()
    }
    type_pages = {}  # TODO.

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
