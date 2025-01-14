from linkml_asciidoc_generator.linkml.model import LinkMLClass, LinkMLEnumeration
from linkml_asciidoc_generator.linkml.model import LinkMLSchema
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.index_page.model import (
    IndexPage,
    Class,
    Enumeration,
)


def _generate_class(class_: LinkMLClass) -> Class:
    return Class(name=class_._meta["name"])


def _generate_enum(enum: LinkMLEnumeration) -> Enumeration:
    return Enumeration(name=enum._meta["name"])


def generate_index_page(schema: LinkMLSchema, config: Config) -> IndexPage:
    index_page = IndexPage(
        name="index",
        title="Index",
        template=config["templates"]["index_page"],
        classes=[_generate_class(c) for c in schema.classes.values()],
        enumerations=[_generate_enum(e) for e in schema.enums.values()],
    )

    return index_page
