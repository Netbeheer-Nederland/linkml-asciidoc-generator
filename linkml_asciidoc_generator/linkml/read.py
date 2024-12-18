from pathlib import Path
import yaml


def read_linkml_schema(schema_file: Path) -> dict:
    with schema_file.open(mode="rb") as f:
        schema_dict = yaml.safe_load(f)

    return schema_dict
