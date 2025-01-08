from linkml_asciidoc_generator.asciidoc import AsciiDocStr
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.type_page.model import TypePage


def render_type_page(type_page: TypePage, config: Config) -> AsciiDocStr: ...
