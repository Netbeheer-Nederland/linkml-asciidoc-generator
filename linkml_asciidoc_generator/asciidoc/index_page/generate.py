from linkml_asciidoc_generator.linkml.model import LinkMLSchema
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.index_page.model import IndexPage


def generate_index_page(schema: LinkMLSchema, config: Config) -> IndexPage:
    index_page = IndexPage(
        name="index",
        schema="asdasd",
        title=schema.title or schema.name,
        template=config["templates"]["index_page"],
    )

    return index_page
