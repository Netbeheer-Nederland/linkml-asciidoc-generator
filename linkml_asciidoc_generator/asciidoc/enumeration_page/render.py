from linkml_asciidoc_generator.asciidoc import AsciiDocStr
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.enumeration_page.model import (
    EnumerationPage,
)


def render_enumeration_page(
    enumeration_page: EnumerationPage, config: Config
) -> AsciiDocStr: ...
