from linkml_asciidoc_generator.linkml.model import LinkMLSlot
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.slot_page.model import SlotPage


def generate_slot_page(class_: LinkMLSlot, config: Config) -> SlotPage: ...
