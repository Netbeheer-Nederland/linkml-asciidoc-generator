from typing import NamedTuple, Callable
from linkml_asciidoc_generator.asciidoc.model import (
    AsciiDocStr,
    Resource,
    Jinja2Template,
    Element,
    CURIE,
    Page,
    ResourceName,
    ResourceKind,
    ResourceID,
    HyperLink,
)
from linkml_asciidoc_generator.linkml.model import (
    LinkMLClassName,
    LinkMLPrimitive,
    LinkMLElementName,
)


class Relation(Element):
    destination_class: LinkMLClassName
    inherited_from: LinkMLClassName | None = None
    description: str | None = None
    uri: CURIE | None = None
    min_cardinality: int = 0
    max_cardinalty: int = 999  # TODO


class Attribute(Element):
    data_type: LinkMLPrimitive
    inherited_from: LinkMLClassName | None = None
    description: str | None = None
    uri: CURIE | None = None
    min_cardinality: int = 0
    max_cardinalty: int = 999  # TODO


class Class(NamedTuple):
    name: LinkMLElementName
    is_abstract: bool
    is_mixin: bool
    uri: CURIE
    ancestors: list[LinkMLClassName]
    relations: list[Relation]
    attributes: list[Attribute]


class MermaidDiagram(Resource):
    template: Jinja2Template


class RelationsDiagram(MermaidDiagram):
    class_name: LinkMLClassName


class AttributesDiagram(MermaidDiagram): ...


class ClassPage(Page):
    class_: Class
    curie: Callable[[CURIE], HyperLink]
    ref: Callable[[ResourceName, ResourceKind], ResourceID]
    ancestors: Callable[
        [list[LinkMLClassName]], AsciiDocStr
    ]  # TODO: These callables are not data, and should go to rendering module.
    title: str | None = None
    relations_diagram: RelationsDiagram | None = None
    attributes_diagram: AttributesDiagram | None = None


class EnumerationPage(Page): ...


class TypePage(Page): ...
