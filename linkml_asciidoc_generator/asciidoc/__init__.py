import os.path
from dataclasses import dataclass
from os import PathLike
from enum import Enum, auto

import jinja2

from linkml_asciidoc_generator.linkml.model import LinkMLElementName


type ResourceName = str
type CURIE = str
type CURIEPrefix = str
type URI = str
type Jinja2TemplateFile = PathLike
type Jinja2TemplateStr = str
type AsciiDocStr = str
type RelativeFilePath = str
type AntoraResourceID = str
type ResourceID = RelativeFilePath | AntoraResourceID
type D2DiagramCodeStr = str
type CharEncoding = str
type PrefixesMap = dict[CURIEPrefix, URI]


class PageKind(Enum):
    INDEX_PAGE = auto()
    NAVIGATION_PAGE = auto()
    CLASS_PAGE = auto()
    SLOT_PAGE = auto()
    ENUMERATION_PAGE = auto()
    TYPE_PAGE = auto()


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


def get_page_resource_id(name: ResourceName, kind: PageKind) -> ResourceID:
    match kind:
        case PageKind.CLASS_PAGE:
            page_type = "class"
        case PageKind.SLOT_PAGE:
            page_type = "slot"
        case PageKind.ENUMERATION_PAGE:
            page_type = "enumeration"
        case PageKind.TYPE_PAGE:
            page_type = "type"
        case PageKind.INDEX_PAGE:
            page_type = ""
        case PageKind.NAVIGATION_PAGE:
            page_type = ""
        case _:
            page_type = ""

    return os.path.join(page_type, f"{name}.adoc")


# Render functions.


def _xref_resource(name: ResourceName, kind: PageKind) -> AsciiDocStr:
    resource_id = get_page_resource_id(name, kind)

    return f"xref::{resource_id}[`{name}`]"


def link_curie(curie: CURIE, prefixes: PrefixesMap) -> AsciiDocStr:
    prefix, ncname = curie.split(":")
    base_uri = prefixes[prefix]

    return f"{base_uri}{ncname}[`{curie}`]"


def xref_class(class_name: ResourceName) -> AsciiDocStr:
    return _xref_resource(class_name, PageKind.CLASS_PAGE)


def xref_enum(enum_name: ResourceName) -> AsciiDocStr:
    return _xref_resource(enum_name, PageKind.ENUMERATION_PAGE)


def xref_slot(
    slot_name: ResourceName,
) -> AsciiDocStr:
    return _xref_resource(slot_name, PageKind.SLOT_PAGE)


def xref_type(type_name: ResourceName) -> AsciiDocStr:
    return _xref_resource(type_name, PageKind.TYPE_PAGE)
