from linkml_asciidoc_generator.linkml.model import LinkMLSchema
from linkml_asciidoc_generator.asciidoc.model.linkml_documentation import (
    LinkMLDocumentation,
)


def generate_linkml_documentation(schema: LinkMLSchema) -> LinkMLDocumentation: ...
