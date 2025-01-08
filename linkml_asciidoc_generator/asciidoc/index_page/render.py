from linkml_asciidoc_generator.asciidoc import AsciiDocStr
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.index_page.model import (
    IndexPage,
)


def render_index_page(index_page: IndexPage, config: Config) -> AsciiDocStr: ...
