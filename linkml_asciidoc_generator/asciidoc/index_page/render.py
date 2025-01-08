from linkml_asciidoc_generator.asciidoc import (
    AsciiDocStr,
    Jinja2TemplateStr,
    read_jinja2_template,
)
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.index_page.model import (
    IndexPage,
)


def render_index_page(index_page: IndexPage, config: Config) -> AsciiDocStr:
    template: Jinja2TemplateStr = read_jinja2_template(
        config["templates"]["index_page"]
    )
    content = template.render(page=index_page)

    return content