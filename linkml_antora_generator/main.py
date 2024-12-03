import linkml_prof_logical_model as linkml_lang
import yaml
from rich import print as pprint
from jinja2 import Environment, FileSystemLoader
import textwrap


# SCHEMA = "data/TC57CIM.IEC61970.yaml"
SCHEMA = "data/core-equipment.yaml"
# SCHEMA = (
#     "/home/bart/Programming/Netbeheer-Nederland/linkml-lang/spec/meta.yaml"
# )
CIM_DATA_TYPES = [
    "VoltagePerReactivePower",
    "Length",
    "ConductancePerLength",
    "VolumeFlowRate",
    "Volume",
    "Voltage",
    "Temperature",
    "Admittance",
    "Impedance",
    "CostPerVolume",
    "SusceptancePerLength",
    "Money",
    "Minutes",
    "CostPerEnergyUnit",
    "FloatQuantity",
    "PerCent",
    "ApparentPower",
    "WaterLevel",
    "Displacement",
    "Damping",
    "Seconds",
    "ResistancePerLengt",
    "Inductance",
    "AngleDegrees",
    "CostRate",
    "Speed",
    "Capacitance",
    "PU",
    "Pressure",
    "KiloActivePower",
    "ReactivePower",
    "ActivePowerChangeRate",
    "Hours",
    "StringQuantity",
    "Conductance",
    "RotationSpeed",
    "CurrentFlow",
    "Frequency",
    "AngleRadians",
    "ActivePower",
    "ReactancePerLength",
    "Resistance",
    "Reactance",
    "Susceptance",
    "RealEnergy",
    "Classification",
    "HeatRate",
    "Emission",
    "CostPerHeatUnit",
    "ActivePowerPerFrequency",
    "InductancePerLength",
    "CapacitancePerLength",
    "ActivePowerPerCurrentFlow",
    "Mass",
]


def class_type(class_):
    if class_.abstract and class_.mixin:
        return "Abstract mixin class"
    elif class_.abstract:
        return "Abstract class"
    elif class_.mixin:
        return "Mixin class"
    else:
        return "Class"


def super_classes(schema, class_name):
    class_ = schema.classes[class_name]

    super_classes = []
    next_class_name = class_.is_a
    while next_class_name:
        if next_class_name:
            super_classes.append(next_class_name)
            next_class_name = schema.classes[next_class_name].is_a
        else:
            break

    return super_classes


def materialize(schema, class_name):
    class_ = schema.classes[class_name].model_copy()

    inherited_attrs = {}
    for super_class_name in super_classes(schema, class_name)[::-1]:
        super_class = schema.classes[super_class_name]
        if super_class.attributes:
            inherited_attrs.update(super_class.attributes)

    if not inherited_attrs:
        return class_

    if not class_.attributes:
        class_.attributes = {}

    class_.attributes.update(inherited_attrs)

    return class_


def render_curie(schema, curie, as_curie=True):
    prefix, local_name = curie.split(":")
    base_uri = schema.prefixes[prefix]
    loc = f"{base_uri}{local_name}"

    if as_curie:
        return f"{loc}[{prefix}:{local_name}]"
    else:
        return f"{loc}[{loc}]"


def _is_relationship(attr):
    return attr.range in schema.classes and attr.range not in CIM_DATA_TYPES


def _get_card(attr):
    if attr.required and attr.multivalued:
        return "1..*"
    elif attr.required and not attr.multivalued:
        return "1"
    elif not attr.required and attr.multivalued:
        return "*"
    else:  # not attr.required and not attr.multivalued
        return "0..1"


def render_mermaid_relations(schema, class_name):
    class_ = schema.classes[class_name]

    attrs = class_.attributes
    if attrs is None:
        attrs = {}

    erd = textwrap.dedent(
        """
    %%{
        init: {
            'theme': 'base',
            'themeVariables': {
            'primaryColor': '#CBDCEB',
            'primaryTextColor': '#000000',
            'primaryBorderColor': '#CBDCEB',
            'lineColor': '#000',
            'secondaryColor': '#006100',
            'tertiaryColor': '#fff',
            'fontSize': '12px'
            }
        }
    }%%\n"""
    )
    erd += "classDiagram\n"
    for attr_name, attr in attrs.items():
        if not _is_relationship(attr):
            continue

        erd += f'\t{class_name} --> "{_get_card(attr)}" {attr.range}: {attr_name}\n'
    return erd


def render_mermaid_class(schema, class_name):
    class_ = schema.classes[class_name]

    attrs = class_.attributes
    if attrs is None:
        attrs = {}

    erd = textwrap.dedent(
        """
        %%{
            init: {
                'theme': 'base',
                'themeVariables': {
                'primaryColor': '#CBDCEB',
                'primaryTextColor': '#000000',
                'primaryBorderColor': '#CBDCEB',
                'lineColor': '#000',
                'secondaryColor': '#006100',
                'tertiaryColor': '#fff',
                'fontSize': '12px'
                }
            }
        }%%\n"""
    )
    erd += "erDiagram\n"
    erd += f"\t{class_name} {{\n"
    for attr_name, attr in attrs.items():
        if _is_relationship(attr):
            continue

        erd += f'\t\t{attr_name} {attr.range} "{_get_card(attr)}"\n'
    return erd + "}"


if __name__ == "__main__":
    with open(SCHEMA, mode="rb") as f:
        schema_dict = yaml.safe_load(f)
        schema = linkml_lang.SchemaDefinition.model_validate(schema_dict)

    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("class.adoc.jinja2")

    # class_name = "expression"
    class_name = "PotentialTransformer"
    class_ = schema.classes[class_name]
    class_uri = (
        render_curie(schema, class_.class_uri, as_curie=True)
        if class_.class_uri
        else None
    )
    schema.classes[class_name] = materialize(schema, class_name)
    class_mermaid_relations = render_mermaid_relations(schema, class_name)
    class_mermaid_class = render_mermaid_class(schema, class_name)

    print(
        template.render(
            class_name=class_name,
            class_=class_,
            class_type=class_type(class_),
            class_uri=class_uri,
            class_mermaid_relations=class_mermaid_relations,
            class_mermaid_class=class_mermaid_class,
            default_prefix=schema.default_prefix,
        )
    )
