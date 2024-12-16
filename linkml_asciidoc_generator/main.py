from pathlib import Path
from linkml_asciidoc_generator.model.asciidoc.linkml_documentation import (
    LinkMLDocumentation,
)
from linkml_asciidoc_generator.model import Config


def create_linkml_documentation(schema_file: Path, config=Config) -> None:
    schema_dict = read_linkml_schema(schema_file)
    schema = parse_linkml_schema(schema_dict)
    linkml_documentation = generate_linkml_documentation(schema)
    # linkml_documentation_adoc = serialize_linkml_documentation(linkml_documentation)
    # write_linkml_documentation(linkml_documentation_adoc)


if __name__ == "__main__":
    config = {}
    schema = Path("data/TC57CIM.yml")
    create_linkml_documentation(schema, config=config)
