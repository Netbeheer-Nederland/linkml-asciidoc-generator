from collections.abc import Callable
from enum import Enum, auto
from os import PathLike
from typing import Any, NamedTuple, NewType, Self, TypedDict

from linkml_antora_generator.linkml.types import (
    LinkMLAttribute,
    LinkMLClass,
    LinkMLClassName,
    LinkMLPrimitiveType,
    LinkMLSlot,
    LinkMLSlotOwner,
)

AsciiDocStr = NewType("AsciiDocStr", str)
Jinja2Template = NewType("Jinja2Template", str)
AsciiDocTemplate = Jinja2Template
AntoraResourceID = NewType("AntoraResourceID", str)
MermaidDiagramCodeStr = NewType("MermaidDiagramCodeStr", str)
AntoraNavigation = NewType("AntoraNavigation", str)


# TODO: Narrow the type down. But what will become its representation?
AntoraImage = NewType("AntoraImage", Any)
AntoraAttachment = NewType("AntoraAttachment", Any)
AntoraExample = NewType("AntoraExample", Any)
AntoraPartial = NewType("AntoraPartial", AsciiDocStr)


class AntoraResourceIDFamilyCoordinate(Enum):
    ATTACHMENT = "attachment$"
    EXAMPLE = "example$"
    IMAGE = "image$"
    PAGE = "page$"
    PARTIAL = "partial$"


class AntoraResourceID(NamedTuple):
    version: str
    file: PathLike
    family: AntoraResourceIDFamilyCoordinate
    module: str
    component: str

    def __str__(self):
        resource_id_str = ""
        if version is not None:
            resource_id_str += f"{version}@"

        return f"{version}@{component}:{module}:{family}${file}"


# TODO: Improve the name of this type. It is tightly coupled to LinkML, which the name does not lay bare.
class AntoraResourceKind(Enum):
    CLASS_PAGE = auto()
    ENUM_PAGE = auto()
    TYPE_PAGE = auto()
    SLOT_PAGE = auto()
    CLASS_RELATIONS_DIAGRAM = auto()
    NAV_PAGE = auto()


class LinkMLClassPageRelationModel(NamedTuple):
    name: str
    uri: str
    min_cardinality: int
    max_cardinalty: int
    destination_class: LinkMLClassName
    description: str
    inherited_from: LinkMLClassName
    xref_func: Callable[[str], str]  # TODO: Is this really it?


class LinkMLClassPageSlotModel(NamedTuple):
    name: str
    uri: str
    min_cardinality: int = 0
    max_cardinalty: int = 999  # TODO: ...
    data_type: LinkMLPrimitiveType
    description: str
    inherited_from: LinkMLClassName


class LinkMLClassAntoraModel(NamedTuple):
    name: str
    is_abstract: bool
    is_mixin: bool
    uri: str
    ancestry: list[LinkMLClassName]
    relations: list[LinkMLClassPageRelationModel]
    attributes: list[LinkMLClassPageSlotModel]

    @classmethod
    def from_linkml_class(cls, source: LinkMLClass) -> Self: ...


class ClassAntoraPageParameters(TypedDict):
    title: str
    class_model: LinkMLClassAntoraModel
    relations_diagram: MermaidDiagramCodeStr
    attributes_diagram: MermaidDiagramCodeStr
    curie: Callable[[str], str]
    ref: Callable[[str], str]


class ClassAntoraPage(NamedTuple):
    name: str
    asciidoc_template: AsciiDocTemplate
    params: ClassAntoraPageParameters


class AntoraConfig(NamedTuple):
    template_map: dict[AntoraResourceKind, PathLike]  # TODO: Nav file too! If empty or missing: no nav for module.
    include_relations_diagram: bool = False
    include_attributes_diagram: bool = False
    module_name: str | None = None


type AntoraPage = ClassAntoraPage | SlotAntoraPage | EnumerationAntoraPage | TypeAntoraPage | AntoraNavigation
AntoraResource = AntoraPage | AntoraImage | AntoraAttachment | AntoraExample | AntoraPartial


class AntoraNavigation:
    name: str
    asciidoc_template: AsciiDocTemplate
    params: ...


class AntoraModule(NamedTuple):
    name: str
    pages: dict[AntoraResourceID, AntoraPage]
    images: dict[AntoraResourceID, AntoraImage]
    attachments: dict[AntoraResourceID, AntoraAttachment]
    examples: dict[AntoraResourceID, AntoraExample]
    partials: dict[AntoraResourceID, AntoraPartial]
    navigation: dict[AntoraResourceID, AntoraNavigation]
