from linkml_asciidoc_generator.linkml.model import (
    LinkMLSchema,
    LinkMLClass,
    LinkMLClassName,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.navigation_page.model import NavigationPage


def _get_classes(schema: LinkMLSchema) -> dict[LinkMLClassName, LinkMLClass]:
    classes = {}
    for class_name, class_ in schema.classes.items():
        if not (class_.annotations and class_.annotations["cim_datatype"]):
            classes[class_name] = class_

    return classes


def generate_navigation_page(schema: LinkMLSchema, config: Config) -> NavigationPage:
    navigation_page = NavigationPage(
        name="nav",
        title="Navigation",
        template=config["templates"]["navigation_page"],
        classes=_get_classes(schema),
        types=[],
    )

    return navigation_page
