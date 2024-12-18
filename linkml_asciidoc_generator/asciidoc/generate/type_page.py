from linkml_asciidoc_generator.model.linkml import LinkMLType
from linkml_asciidoc_generator.model.asciidoc import Config
from linkml_asciidoc_generator.model.asciidoc.type_page import TypePage


def generate_class_page(class_: LinkMLType, config: Config) -> TypePage: ...
