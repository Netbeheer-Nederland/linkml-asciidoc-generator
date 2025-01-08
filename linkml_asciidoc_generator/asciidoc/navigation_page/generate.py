from linkml_asciidoc_generator.linkml.model import LinkMLSchema
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.navigation_page.model import NavigationPage


def generate_navigation_page(schema: LinkMLSchema, config: Config) -> NavigationPage:
    navigation_page = NavigationPage(
        name="nav",
        title="Navigation",
        template=config["templates"]["navigation_page"],
    )

    return navigation_page
