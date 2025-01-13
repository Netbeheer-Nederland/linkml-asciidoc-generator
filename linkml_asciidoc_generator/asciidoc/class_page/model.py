from dataclasses import dataclass
from enum import Enum
from linkml_asciidoc_generator.asciidoc import (
    Resource,
    Jinja2TemplateFile,
    Element,
    CURIE,
    Page,
    PrefixesMap,
)
from linkml_asciidoc_generator.linkml.model import (
    LinkMLClassName,
    LinkMLPrimitive,
    LinkMLElementName,
)


type PositiveInt = int


class CIMStandard(Enum):
    IEC61970 = "IEC61970"
    IEC61968 = "IEC61968"
    IEC62325 = "IEC62325"


@dataclass
class Relation(Element):
    destination_class: "Class"
    inherited_from: LinkMLClassName | None = None
    description: str | None = None
    uri: CURIE | None = None
    min_cardinality: int = 0
    max_cardinalty: PositiveInt | None = None


@dataclass
class Attribute(Element):
    data_type: LinkMLPrimitive
    inherited_from: LinkMLClassName | None = None
    description: str | None = None
    uri: CURIE | None = None
    min_cardinality: int = 0
    max_cardinalty: PositiveInt | None = None


@dataclass
class Class:
    name: LinkMLElementName
    is_abstract: bool
    is_mixin: bool
    is_cim_data_type: bool
    uri: CURIE
    ancestors: list[LinkMLClassName]
    relations: list[Relation]
    attributes: list[Attribute]
    prefixes: PrefixesMap
    standard: CIMStandard | None = None
    description: str | None = None


@dataclass
class D2Diagram(Resource):
    template: Jinja2TemplateFile


@dataclass
class RelationsDiagram(D2Diagram):
    class_: Class


@dataclass
class ClassPage(Page):
    class_: Class
    relations_diagram: RelationsDiagram | None = None
