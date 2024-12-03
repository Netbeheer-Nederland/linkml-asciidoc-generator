import linkml_prof_logical_model as linkml_lang
import yaml
from jinja2 import Environment, FileSystemLoader
import textwrap
from pathlib import Path

import linkml_antora_generator.schema as Schema
from linkml_antora_generator.generator import AntoraDocsGenerator


def cim_class_color(class_: ClassDefinition) -> str:
    package = str(urlparse(class_.from_schema).fragment)
    top_level_package = ".".join(package.split(".")[:2])

    return {
        "TC57CIM.IEC61970": "rgb(236, 207, 203)",
        "TC57CIM.IEC61968": "rgb(209, 231, 194)",
        "TC57CIM.IEC62325": "rgb(255, 251, 239)",
    }[top_level_package]


if __name__ == "__main__":
    data_dir = Path("data")

    # Single schema.
    schemas = {Schema.read(data / "im_capaciteitskaart-full.yaml")}
    adocgen = AntoraDocsGenerator(schemas, class_color=cim_class_color)

    # Multiple schemas.
    schemas = {Schema.read(schema_file) for schema_file in {data / "im_capaciteitskaart-full.yaml", data / "TC57CIM.IEC61970.yaml"}}
    adocgen = AntoraDocsGenerator(schemas, class_color=cim_class_color, metadata={"name": "nbnl-cim-profile-group", "title": "NBNL CIM Profile Group"})

    # Run.
    adocgen.create_docs()
