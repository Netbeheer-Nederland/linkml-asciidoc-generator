from linkml_asciidoc_generator.model.linkml import LinkMLClass
from linkml_asciidoc_generator.model.asciidoc import Config
from linkml_asciidoc_generator.model.asciidoc.class_page import ClassPage


def generate_class_page(class_: LinkMLClass, config: Config) -> ClassPage: ...
