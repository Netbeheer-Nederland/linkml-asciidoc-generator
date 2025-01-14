from linkml_asciidoc_generator.linkml.model import LinkMLClass, LinkMLEnumeration
from linkml_asciidoc_generator.linkml.model import LinkMLSchema
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc import is_cim_data_type
from linkml_asciidoc_generator.asciidoc.index_page.model import (
    IndexPage,
    Class,
    CIMDataType,
    Enumeration,
)


def _generate_class(class_: LinkMLClass) -> Class:
    return Class(name=class_._meta["name"], description=class_.description)


def _generate_cim_data_type(class_: LinkMLClass) -> CIMDataType:
    return Class(name=class_._meta["name"], description=class_.description)


def _generate_enum(enum: LinkMLEnumeration) -> Enumeration:
    return Enumeration(name=enum._meta["name"], description=enum.description)


def generate_index_page(schema: LinkMLSchema, config: Config) -> IndexPage:
    index_page = IndexPage(
        name="index",
        title="Index",
        template=config["templates"]["index_page"],
        classes=[
            _generate_class(c)
            for c in filter(lambda c: not is_cim_data_type(c), schema.classes.values())
        ],
        cim_data_types=[
            _generate_cim_data_type(c)
            for c in filter(is_cim_data_type, schema.classes.values())
        ],
        enumerations=[_generate_enum(e) for e in schema.enums.values()],
    )

    return index_page
