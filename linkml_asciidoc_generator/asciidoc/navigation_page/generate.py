from linkml_asciidoc_generator.linkml.model import (
    LinkMLSchema,
)
from linkml_asciidoc_generator.asciidoc import ResourceName
from linkml_asciidoc_generator.asciidoc.class_page.model import Class
from linkml_asciidoc_generator.asciidoc.class_page.generate import generate_class
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.navigation_page.model import NavigationPage


def _get_classes(schema: LinkMLSchema, config: Config) -> dict[ResourceName, Class]:
    classes = {}
    for class_name, class_ in schema.classes.items():
        if not (class_.annotations and class_.annotations["cim_datatype"]):
            classes[class_name] = generate_class(class_, schema, config)

    return classes


def generate_navigation_page(schema: LinkMLSchema, config: Config) -> NavigationPage:
    navigation_page = NavigationPage(
        name="nav",
        title="Navigation",
        template=config["templates"]["navigation_page"],
        classes=_get_classes(schema, config),
        types=[],
    )

    return navigation_page
