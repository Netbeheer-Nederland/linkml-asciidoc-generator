from linkml_asciidoc_generator.asciidoc import (
    AsciiDocStr,
    read_jinja2_template,
    xref_class,
    Jinja2TemplateStr,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.navigation_page.model import (
    NavigationPage,
)


def render_navigation_page(
    navigation_page: NavigationPage, config: Config
) -> AsciiDocStr:
    template: Jinja2TemplateStr = read_jinja2_template(
        config["templates"]["navigation_page"]
    )
    content = template.render(page=navigation_page, xref_class=xref_class)

    return content
