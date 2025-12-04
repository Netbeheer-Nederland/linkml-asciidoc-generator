import argparse
import sys

from pathlib import Path
from linkml_asciidoc_generator.linkml.read import read_linkml_schema
from linkml_asciidoc_generator.linkml.parse import parse_linkml_schema
from linkml_asciidoc_generator.asciidoc.linkml_documentation.generate import (
    generate_linkml_documentation,
)
from linkml_asciidoc_generator.asciidoc.linkml_documentation.render import (
    render_linkml_documentation,
)
from linkml_asciidoc_generator.asciidoc.linkml_documentation.write import (
    write_linkml_documentation,
)
from linkml_asciidoc_generator.config import Config


def create_linkml_documentation(schema_file: Path, config: Config) -> None:
    schema_dict = read_linkml_schema(schema_file)
    schema = parse_linkml_schema(schema_dict)
    linkml_documentation = generate_linkml_documentation(schema, config)
    linkml_documentation_adoc = render_linkml_documentation(
        linkml_documentation, config
    )
    write_linkml_documentation(linkml_documentation_adoc, config)

    # pprint(linkml_documentation.class_pages["MarketEvaluationPoint"].relations_diagram)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", help="path to the LinkML schema", type=Path)
    parser.add_argument("-o", "--output-dir", help="output directory path to write Antora module to", default=Path("./output"), type=Path)
    parser.add_argument("-t", "--templates-dir", help="path to (custom) Jinja2 templates for rendering the AsciiDco", default=Path(__file__).parent / 'asciidoc' / 'templates', type=Path)
    parser.add_argument("--render-diagrams", help="whether to render relation diagrams or not", action="store_true")

    args = parser.parse_args()

    config = {
        "templates": {
            "dir": args.templates_dir,
            "class_page": "class_page/class_page.adoc.jinja2",
            "enumeration_page": "enumeration_page.adoc.jinja2",
            "cim_data_type_page": "class_page/cim_data_type_page.adoc.jinja2",
            "class_page_relations_diagram": "class_page/relations_diagram.adoc.jinja2",
            "index_page": "index_page.adoc.jinja2",
            "navigation_page": "navigation_page.adoc.jinja2",
        },
        "diagrams": {
            "relations": args.render_diagrams,
            "class_color": {
                "IEC61970 (Grid)": "#eccfcb",
                "IEC61968 (Enterprise)": "#d1e7c2",
                "IEC62325 (Market)": "#fffbef",
            },
        },
        "output_dir": args.output_dir,
        "char_encoding": "utf8",
    }

    create_linkml_documentation(args.schema, config=config)
