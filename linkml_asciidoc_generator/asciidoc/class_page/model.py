from dataclasses import dataclass
from linkml_asciidoc_generator.asciidoc import (
    Resource,
    Jinja2TemplateFile,
    Element,
    CURIE,
    Page,
    PrefixesMap,
    SkosMapping,
    CIMStandard,
)
from linkml_asciidoc_generator.linkml.model import (
    LinkMLClassName,
    LinkMLPrimitive,
    LinkMLElementName,
)

type PositiveInt = int


@dataclass
class Slot(Element):
    pass


@dataclass
class Relation(Slot):
    destination_class: "Class"
    inherited_from: LinkMLClassName | None = None
    description: str | None = None
    uri: CURIE | None = None
    min_cardinality: int = 0
    max_cardinality: PositiveInt | None = None
    skos_mappings: SkosMapping | None = None


@dataclass
class Attribute(Slot):
    data_type: LinkMLPrimitive
    inherited_from: LinkMLClassName | None = None
    description: str | None = None
    uri: CURIE | None = None
    min_cardinality: int = 0
    max_cardinality: PositiveInt | None = None
    skos_mappings: SkosMapping | None = None


@dataclass
class Class:
    name: LinkMLElementName
    ancestors: list[LinkMLClassName]
    relations: list[Relation]
    attributes: list[Attribute]
    prefixes: PrefixesMap
    uri: CURIE | None = None
    is_abstract: bool = False
    is_mixin: bool = False
    is_cim_data_type: bool = False
    is_root: bool = False
    standard: CIMStandard | None = None
    description: str | None = None
    skos_mappings: SkosMapping | None = None


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
