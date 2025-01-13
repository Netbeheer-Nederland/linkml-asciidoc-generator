from linkml_asciidoc_generator.linkml.model import LinkMLType
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.type_page.model import TypePage


def generate_type_page(class_: LinkMLType, config: Config) -> TypePage: ...
