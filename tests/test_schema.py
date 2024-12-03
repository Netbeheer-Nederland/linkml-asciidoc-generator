import pytest
import linkml_antora_generator.schema as schema

# import linkml_antora_generator.linkml_prof_logical_model as linkml_type
import linkml_antora_generator.linkml_full as linkml_type
import yaml

# CLASS_ = linkml_type.ClassDefinition()
# SCHEMA = linkml_type.SchemaDefinition(
# id="http://example.org/schema/1", classes={"A": CLASS_}
# )

# SCHEMA = "data/TC57CIM.IEC61970.yaml"
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


# @pytest.fixture
# def schema():
#     linkml_file = "data/core-equipment.yaml"
#     with open(linkml_file, mode="rb") as f:
#         schema_dict = yaml.safe_load(f)
#         print(schema_dict["name"])
#         _schema = linkml_type.SchemaDefinition.model_validate(schema_dict)

#     return _schema


#def test_init():
#    schema_dict = {
#        "id": "http://data.example.org/schema/music-library",
#        "name": "music-library",
#        "classes": {
#            "Artist": {
#                "attributes": {"plays": {"range": "Instrument"}},
#                "slots": ["name"],
#                "slot_usage": {"name": {"required": True}},
#            }
#        },
#    }
#    schema_ = schema.init(schema_dict)
#
#    from operator import attrgetter, itemgetter
#
#    print([c._meta["name"] for c in schema_.classes.values()])


# def test_get_ancestors(schema):
#     potential_transformer = Schema.get_class("PotentialTransformer", schema)
#     as_ = [c.class_uri for c in Schema.get_ancestors(potential_transformer, schema)]
#     #print(potential_transformer._name)
#     print(as_)
