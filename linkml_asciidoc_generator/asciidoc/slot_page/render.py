from linkml_asciidoc_generator.asciidoc import AsciiDocStr
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.slot_page.model import (
    SlotPage,
)


def render_slot_page(slot_page: SlotPage, config: Config) -> AsciiDocStr: ...
