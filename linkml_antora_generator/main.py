import linkml_prof_logical_model as linkml_lang
import yaml
from jinja2 import Environment, FileSystemLoader
import textwrap

import linkml_antora_generator.schema as Schema
from linkml_antora_generator.generator import AntoraDocsGenerator, cim_class_color


if __name__ == "__main__":
    schema_file = "data/im_capaciteitskaart-full.yaml"

    with open(schema_file, mode="rb") as f:
        schema_dict = yaml.safe_load(f)
        schema = linkml_lang.SchemaDefinition.model_validate(schema_dict)

    schema = Schema.read(schema_file)
    adocgen = AntoraDocsGenerator(schema, cim_class_color)
    adocgen.create_docs()
