from pathlib import Path
from linkml_asciidoc_generator.model.linkml import LinkMLSchema
from linkml_asciidoc_generator.model.asciidoc.linkml_documentation import (
    LinkMLDocumentation,
)
from linkml_asciidoc_generator.model import Config
import yaml


def _set_names(elements) -> None:
    for name, el in elements.items():
        el._meta["name"] = name


def read_linkml_schema(schema_file: Path) -> dict:
    with schema_file.open(mode="rb") as f:
        schema_dict = yaml.safe_load(f)

    return schema_dict


def parse_linkml_schema(schema_dict: dict) -> LinkMLSchema:
    schema = LinkMLSchema.model_validate(schema_dict)

    # Set name for elements.
    _set_names(schema.classes or {})
    _set_names(schema.slots or {})
    _set_names(schema.types or {})
    _set_names(schema.enums or {})
    _set_names(schema.subsets or {})

    # Set name for slots and attributes used in classes.
    for class_ in (schema.classes or {}).values():
        _set_names(class_.attributes or {})
        _set_names(class_.slot_usage or {})

    return schema


def generate_linkml_documentation(schema: LinkMLSchema) -> LinkMLDocumentation: ...


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
