import pytest
import textwrap
from linkml_antora_generator.generator import AntoraDocsGenerator, cim_class_color
import linkml_antora_generator.schema as Schema
from cssutils.scripts import csscombine
from pprint import pprint

from xml.etree import ElementTree


# def test_():
#     schema_dict = {
#         "id": "http://data.example.org/schema/music-library",
#         "name": "music-library",
#         "classes": {
#             "Artist": {
#                 "attributes": {"plays": {"range": "Instrument"}},
#                 "slots": ["name"],
#                 "slot_usage": {"name": {"required": True}},
#             }
#         },
#     }
#     schema = Schema.init(schema_dict)
#     adocgen = AntoraDocsGenerator(schema)


def test_pages():
    #schema_file = "data/TC57CIM.yml"
    schema_file = "data/im_capaciteitskaart-full.yaml"
    schema = Schema.read(schema_file)
    adocgen = AntoraDocsGenerator(schema, cim_class_color)

    #identified_object = schema.classes["IdentifiedObject"]
    #name = schema.classes["Name"]
    #potential_transformer = schema.classes["PotentialTransformer"]
    #power_transformer = schema.classes["PowerTransformer"]
    #wire_position = schema.classes["WirePosition"]
    #busbar_section = schema.classes["BusbarSection"]

    #adocgen.create_class_page(identified_object)
    #adocgen.create_class_page(name)
    #adocgen.create_class_page(potential_transformer)
    #adocgen.create_class_page(power_transformer)
    #adocgen.create_class_page(wire_position)
    #adocgen.create_class_page(busbar_section)

    #unit_symbol = schema.enums["UnitSymbol"]
    #adocgen.create_enum_page(unit_symbol)

    for class_ in schema.classes.values():
        adocgen.create_class_page(class_)

    for enum in schema.enums.values():
        adocgen.create_enum_page(enum)

    adocgen.create_nav_page()


# def test_svg():
#     svg_file = (
#         "output/modules/ROOT/images/PowerElectronicsConnection_relations.svg"
#     )
#     # with open(svg_file, mode="rb") as f:
#     svg_root_el = parse_svg(svg_file)


# svg_dom = xml.dom.minidom.parseString(svg)
# style_node = svg_dom.getElementsByTagName("style")[
#     0
# ].firstChild.replaceChild("asdasdassdas")
# nodes = svg_dom.childNodes


#    sheet = cssutils.parseString(style.nodeValue)
#    for rule in sheet:
#        if rule.selectorText == "#PowerElectronicsConnection_relations .edgeLabel .label span":
#            print(dir(rule.style))
# print(
#     csscombine(
#         cssText="""body {
#     background-color: red;


#                  }
#                  """
#     )
# )

# class_adoc = adocgen.class_page(schema.classes["Artist"], schema)
# print(class_adoc)


#     diagram_code = textwrap.dedent(
#         """classDiagram
#     class Potential
#     PotentialTransformer : description string 0..1
#     PotentialTransformer : energyIdentCodeEic string 0..1
#     PotentialTransformer : mRID string 1
#     PotentialTransformer : name string 1
#     PotentialTransformer : shortName string 0..1
#     PotentialTransformer : aggregate boolean 0..1
#     PotentialTransformer : normallyInService boolean 0..1

#     PotentialTransformer --> "0..1" EquipmentContainer: EquipmentContainer
#     PotentialTransformer --> "*" OperationalLimitSet: OperationalLimitSet
#     PotentialTransformer --> "1" Terminal: Terminal
# """
#     )
#     adocgen.render_mermaid(diagram_code)
# print(diagram_code)
