from linkml_asciidoc_generator.model.linkml import LinkMLEnumeration
from linkml_asciidoc_generator.model.asciidoc import Config
from linkml_asciidoc_generator.model.asciidoc.enumeration_page import EnumerationPage


def generate_enumeration_page(
    class_: LinkMLEnumeration, config: Config
) -> EnumerationPage: ...
