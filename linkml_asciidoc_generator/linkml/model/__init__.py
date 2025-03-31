from enum import Enum
from typing import NewType

from linkml_asciidoc_generator.linkml.model.metamodel import (
    Element,
    ClassDefinition,
    EnumDefinition,
    TypeDefinition,
    SlotDefinition,
    SchemaDefinition,
    PermissibleValue,
)

LinkMLElement = Element
LinkMLClass = ClassDefinition
LinkMLEnumeration = EnumDefinition
LinkMLEnumerationValue = PermissibleValue
LinkMLType = TypeDefinition

LinkMLSlot = SlotDefinition
LinkMLAttribute = NewType("LinkMLAttribute", LinkMLSlot)

LinkMLSchema = SchemaDefinition

LinkMLElementName = str
LinkMLSlotName = str
LinkMLClassName = str
LinkMLSlotOwner = ClassDefinition


class LinkMLPrimitive(Enum):
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DOUBLE = "double"
    DECIMAL = "decimal"
    TIME = "time"
    DATE = "date"
    DATETIME = "datetime"
    DATE_OR_DATETIME = "date_or_datetime"
    URI_OR_CURIE = "uriorcurie"
    CURIE = "curie"
    URI = "uri"
    NCNAME = "ncname"
    OBJECT_IDENTIFIER = "objectidentifier"
    NODE_IDENTIFIER = "nodeidentifier"
    JSON_POINTER = "jsonpointer"
    JSON_PATH = "jsonpath"
    SPARQL_PATH = "sparqlpath"
