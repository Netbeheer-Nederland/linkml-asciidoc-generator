from dataclasses import dataclass
from linkml_asciidoc_generator.asciidoc import (
    Resource,
    Jinja2TemplateFile,
    Element,
    CURIE,
    Page,
)
from linkml_asciidoc_generator.linkml.model import (
    LinkMLClassName,
    LinkMLPrimitive,
    LinkMLElementName,
)


@dataclass
class Relation(Element):
    destination_class: LinkMLClassName
    inherited_from: LinkMLClassName | None = None
    description: str | None = None
    uri: CURIE | None = None
    min_cardinality: int = 0
    max_cardinalty: int = 999  # TODO


@dataclass
class Attribute(Element):
    data_type: LinkMLPrimitive
    inherited_from: LinkMLClassName | None = None
    description: str | None = None
    uri: CURIE | None = None
    min_cardinality: int = 0
    max_cardinalty: int = 999  # TODO


@dataclass
class Class:
    name: LinkMLElementName
    is_abstract: bool
    is_mixin: bool
    uri: CURIE
    ancestors: list[LinkMLClassName]
    relations: list[Relation]
    attributes: list[Attribute]


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
    # curie: Callable[[CURIE], HyperLink]
    # ref: Callable[[ResourceName, ResourceKind], ResourceID]
    # ancestors: Callable[
    #     [list[LinkMLClassName]], AsciiDocStr
    # ]  # TODO: These callables are not data, and should be parameters in the rendering/serialization module
