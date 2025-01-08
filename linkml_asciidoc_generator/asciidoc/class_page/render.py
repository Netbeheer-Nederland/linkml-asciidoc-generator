from linkml_asciidoc_generator.asciidoc import AsciiDocStr
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.class_page.model import (
    ClassPage,
)


def render_class_page(class_page: ClassPage, config: Config) -> AsciiDocStr: ...
