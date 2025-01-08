from pathlib import Path
from dataclasses import dataclass
from os import PathLike
from enum import Enum, auto

import jinja2

from linkml_asciidoc_generator.linkml.model import LinkMLElementName


type ResourceName = str
type CURIE = str
type HyperLink = str
type Jinja2TemplateFile = PathLike
type Jinja2TemplateStr = str
type AsciiDocStr = str
type RelativeFilePath = str
type AntoraResourceID = str
type ResourceID = RelativeFilePath | AntoraResourceID
type D2DiagramCodeStr = str


class ResourceKind(Enum):
    INDEX_PAGE = auto()
    NAVIGATION_PAGE = auto()
    CLASS_PAGE = auto()
    SLOT_PAGE = auto()
    ENUMERATION_PAGE = auto()
    TYPE_PAGE = auto()
    RELATIONS_DIAGRAM = auto()
    ATTRIBUTES_DIAGRAM = auto()


@dataclass
class Resource:
    name: ResourceName


@dataclass
class Element:
    name: LinkMLElementName


class Page(Resource):
    title: str
    template: Jinja2TemplateFile


def read_jinja2_template(template_name: str, templates_dir: Path) -> Jinja2TemplateStr:
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
    template = jinja2_env.get_template(template_name)

    return template
