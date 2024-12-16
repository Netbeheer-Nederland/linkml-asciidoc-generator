from linkml_asciidoc_generator.model.linkml import LinkMLSchema
from linkml_asciidoc_generator.model.asciidoc.linkml_documentation import (
    LinkMLDocumentation,
)


def generate_linkml_documentation(schema: LinkMLSchema) -> LinkMLDocumentation: ...
