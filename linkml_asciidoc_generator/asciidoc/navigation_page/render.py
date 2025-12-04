from linkml_asciidoc_generator.asciidoc import (
    AsciiDocStr,
    read_jinja2_template,
    xref_class,
    xref_enum,
    Jinja2TemplateStr,
)
from linkml_asciidoc_generator.asciidoc import ResourceName
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.navigation_page.model import (
    NavigationPage,
)
from linkml_asciidoc_generator.asciidoc.class_page.model import Class


def _get_root_class(classes: dict[ResourceName, Class]) -> Class | None:
    for class_ in classes.values():
        if class_.is_root:
            return class_


def render_navigation_page(
    navigation_page: NavigationPage, config: Config
) -> AsciiDocStr:
    template: Jinja2TemplateStr = read_jinja2_template("navigation_page", config)

    content = template.render(
        page=navigation_page,
        root_class=_get_root_class(navigation_page.classes),
        xref_class=xref_class,
        xref_enum=xref_enum,
    )

    return content
