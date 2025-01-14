from linkml_asciidoc_generator.linkml.model import (
    LinkMLSchema,
)
from linkml_asciidoc_generator.asciidoc import ResourceName
from linkml_asciidoc_generator.asciidoc.class_page.model import Class
from linkml_asciidoc_generator.asciidoc.enumeration_page.model import Enumeration
from linkml_asciidoc_generator.asciidoc.class_page.generate import generate_class
from linkml_asciidoc_generator.asciidoc.enumeration_page.generate import (
    generate_enumeration,
)
from linkml_asciidoc_generator.asciidoc.class_page.generate import is_cim_data_type
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.navigation_page.model import NavigationPage


def _get_classes(schema: LinkMLSchema, config: Config) -> dict[ResourceName, Class]:
    classes = {}
    for class_name, class_ in schema.classes.items():
        if not is_cim_data_type(class_):
            classes[class_name] = generate_class(class_, schema, config)

    return classes


def _get_enumerations(
    schema: LinkMLSchema, config: Config
) -> dict[ResourceName, Enumeration]:
    # TODO: Hacky, but works.
    if schema.enums is None:
        linkml_enums = {}
    else:
        linkml_enums = schema.enums

    return {
        enum_name: generate_enumeration(enum, schema)
        for enum_name, enum in linkml_enums.items()
    }


def _get_cim_data_types(
    schema: LinkMLSchema, config: Config
) -> dict[ResourceName, Class]:
    cim_data_types = {}
    for class_name, class_ in schema.classes.items():
        if is_cim_data_type(class_):
            cim_data_types[class_name] = generate_class(class_, schema, config)

    return cim_data_types


def generate_navigation_page(schema: LinkMLSchema, config: Config) -> NavigationPage:
    navigation_page = NavigationPage(
        name="nav",
        title="Navigation",
        template=config["templates"]["navigation_page"],
        classes=_get_classes(schema, config),
        enumerations=_get_enumerations(schema, config),
        cim_data_types=_get_cim_data_types(schema, config),
    )

    return navigation_page
