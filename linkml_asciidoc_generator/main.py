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


def create_linkml_documentation(schema_file: Path, config=Config) -> None:
    schema_dict = read_linkml_schema(schema_file)
    schema = parse_linkml_schema(schema_dict)
    linkml_documentation = generate_linkml_documentation(schema, config)
    linkml_documentation_adoc = render_linkml_documentation(
        linkml_documentation, config
    )
    write_linkml_documentation(linkml_documentation_adoc, config)

    # pprint(linkml_documentation.class_pages["MarketEvaluationPoint"].relations_diagram)


if __name__ == "__main__":
    config = {
        "templates": {
            "class_page": "linkml_asciidoc_generator/templates/class_page/class_page.adoc.jinja2",
            "class_page_relations_diagram": "linkml_asciidoc_generator/templates/class_page/relations_diagram.adoc.jinja2",
            "index_page": "linkml_asciidoc_generator/templates/index_page.adoc.jinja2",
            "navigation_page": "linkml_asciidoc_generator/templates/navigation_page.adoc.jinja2",
        },
        "diagrams": {
            "relations": True,
            "class_color": {
                "IEC61970": "#eccfcb",
                "IEC61968": "#d1e7c2",
                "IEC62325": "#fffbef",
            },
        },
        "output_dir": "output/",
        "char_encoding": "utf8",
    }
    schema = Path("data/dp_nbl_forecast.yaml")
    # schema = Path("data/dp_meetdata.new.yaml")
    create_linkml_documentation(schema, config=config)
