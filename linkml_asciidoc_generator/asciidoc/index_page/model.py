from dataclasses import dataclass
from linkml_asciidoc_generator.asciidoc import Page


@dataclass
class Schema: ...


class IndexPage(Page):
    schema: Schema
