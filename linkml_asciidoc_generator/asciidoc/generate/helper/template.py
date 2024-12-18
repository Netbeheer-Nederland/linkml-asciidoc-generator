from pathlib import Path

import jinja2

from linkml_asciidoc_generator.asciidoc.model import Jinja2Template


def read_jinja2_template(template_name: str, templates_dir: Path) -> Jinja2Template:
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
    template = jinja2_env.get_template(template_name)

    return template
