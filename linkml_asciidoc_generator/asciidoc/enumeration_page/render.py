from functools import partial

from linkml_asciidoc_generator.asciidoc import (
    AsciiDocStr,
    Jinja2TemplateStr,
    read_jinja2_template,
    link_curie,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.enumeration_page.model import (
    EnumerationPage,
)


def render_enumeration_page(
    enumeration_page: EnumerationPage, config: Config
) -> AsciiDocStr:
    template: Jinja2TemplateStr = read_jinja2_template(
        config["templates"]["enumeration_page"]
    )

    content = template.render(
        enumeration=enumeration_page.enumeration,
        link_curie=partial(link_curie, prefixes=enumeration_page.enumeration.prefixes),
    )

    return content
