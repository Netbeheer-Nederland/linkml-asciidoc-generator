from linkml_asciidoc_generator.asciidoc import AsciiDocStr
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.navigation_page.model import (
    NavigationPage,
)


def render_navigation_page(
    navigation_page: NavigationPage, config: Config
) -> AsciiDocStr: ...
