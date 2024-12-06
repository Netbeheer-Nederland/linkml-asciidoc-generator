"""
set[LinkMLSchema] -> AntoraComponentVersion
"""

from linkml_antora_generator.linkml.types import *
from linkml_antora_generator.antora.types import *
from linkml_antora_generator.antora.module import generate_module


def generate_component_version(
    schemas: set[LinkMLSchema], descriptor: AntoraComponentVersionDescriptor, config: AntoraConfig
) -> AntoraComponentVersion:
    modules: set[AntoraModule]

    if len(schemas) == 1:
        modules = {generate_module(schemas[0], name="ROOT", config=config)}
    else:
        modules = {generate_module(s, config=config) for s in schemas}

    return AntoraComponentVersion(descriptor=descriptor, modules=modules)
