from os import PathLike
from typing import NamedTuple, Self

from linkml_antora_generator.linkml.model import *  # Extend the generated model code; don't modify.


type LinkMLClass = ClassDefinition
type LinkMLEnumeration = EnumDefinition
type LinkMLType = TypeDefinition

type LinkMLSlot = SlotDefinition
type LinkMLAttribute = NewType("LinkMLAttribute", LinkMLSlot)

type LinkMLSchema = SchemaDefinition


#class LinkMLProject(NamedTuple):
#    schemas: set[LinkMLSchema]
#    name: str | None = None
#    title: str | None = None
#    root_dir: PathLike | None = None
#
#    @classmethod
#    def from_schema(schema: LinkMLSchema, name=None, title=None, root_dir=None) -> Self:
#        pass
#        
#    @classmethod
#    def from_schema(schema: LinkMLSchema, name=None, title=None, root_dir=None) -> Self:
#        pass
