from linkml_asciidoc_generator.linkml.model import LinkMLEnumeration
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.enumeration_page.model import EnumerationPage


def generate_enumeration_page(
    class_: LinkMLEnumeration, config: Config
) -> EnumerationPage: ...
