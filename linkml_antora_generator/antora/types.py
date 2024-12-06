from enum import Enum, auto
from os import PathLike
from typing import NamedTuple, TypedDict


AsciiDocStr = NewType("AsciiDocStr", str)
AntoraResourceID = NewType("AntoraResourceID", str)
MermaidDiagramCodeStr = NewType("MermaidDiagramCodeStr", str)

# TODO: Narrow the type down. But what will become its representation?
AntoraImage = NewType("AntoraImage", Any)
AntoraAttachment = NewType("AntoraAttachment", Any)
AntoraExample = NewType("AntoraExample", Any)
AntoraPartial = NewType("AntoraPartial", AsciiDocStr)

AntoraResource = AntoraPage | AntoraImage | AntoraAttachment | AntoraExample | AntoraPartial


class AntoraResourceFamily(Enum):
    PAGE = auto()
    IMAGE = auto()
    EXAMPLE = auto()
    ATTACHMENT = auto()
    PARTIAL = auto()


# TODO: Improve the name of this type. It is tightly coupled to LinkML, which the name does not lay bare.
class AntoraResourceType(Enum):
    CLASS_PAGE = auto()
    ENUM_PAGE = auto()
    CLASS_RELATIONS_DIAGRAM = auto()
    NAV_PAGE = auto()


class AntoraPage(NamedTuple):
    content: AsciiDocStr
    mermaid_diagrams: dict[AntoraResourceID, MermaidDiagramCodeStr]
    # TODO: Out of scope for now:
    # partials: dict [AntoraResourceID, AsciiDocStr]


class AntoraComponentVersionDescriptor(NamedTuple):
    name: str
    title: str | None = None
    version: str | None = None
    pre_release: str | None = None
    nav: str = None


class AntoraComponentVersion(NamedTuple):
    descriptor: AntoraComponentVersionDescriptor
    modules: set[AntoraModule]


class AntoraModule(NamedTuple):
    name: str
    pages: set[AntoraPage] | None = None
    images: set[AntoraImage] | None = None
    attachments: set[AntoraAttachment] | None = None
    examples: set[AntoraExample] | None = None
    partials: set[AntoraPartial] | None = None


class AntoraConfig(NamedTuple):
    include_relations_diagram: bool = False
    include_attributes_diagram: bool = False
    template_map: dict[AntoraResourceType, PathLike]
