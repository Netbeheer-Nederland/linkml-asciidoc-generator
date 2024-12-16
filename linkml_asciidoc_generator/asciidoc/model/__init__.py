from enum import Enum, auto
from typing import NamedTuple

from linkml_asciidoc_generator.linkml.model import LinkMLElementName


type ResourceName = str
type CURIE = str
type HyperLink = str
type Jinja2Template = str
type AsciiDocStr = str
type RelativeFilePath = str
type AntoraResourceID = str
type ResourceID = RelativeFilePath | AntoraResourceID


class ResourceKind(Enum):
    INDEX_PAGE = auto()
    NAVIGATION_PAGE = auto()
    CLASS_PAGE = auto()
    SLOT_PAGE = auto()
    ENUMERATION_PAGE = auto()
    TYPE_PAGE = auto()
    RELATIONS_DIAGRAM = auto()
    ATTRIBUTES_DIAGRAM = auto()


class Resource(NamedTuple):
    name: ResourceName


class Element(NamedTuple):
    name: LinkMLElementName


class Page(Resource):
    template: Jinja2Template
