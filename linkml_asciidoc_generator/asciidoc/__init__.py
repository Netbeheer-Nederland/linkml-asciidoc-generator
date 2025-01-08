import os.path
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


@dataclass
class Page(Resource):
    title: str
    template: Jinja2TemplateFile


def read_jinja2_template(template_path: PathLike) -> Jinja2TemplateStr:
    template_dir, tmpl_filename = os.path.split(template_path)
    jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = jinja2_env.get_template(tmpl_filename)

    return template
