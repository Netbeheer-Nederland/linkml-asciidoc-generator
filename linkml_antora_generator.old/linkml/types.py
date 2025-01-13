from typing import NewType

from linkml_antora_generator.linkml.model import *  # Extend the generated model code; don't modify.

type LinkMLClass = ClassDefinition
type LinkMLEnumeration = EnumDefinition
type LinkMLType = TypeDefinition

type LinkMLSlot = SlotDefinition
LinkMLAttribute = NewType("LinkMLAttribute", LinkMLSlot)

type LinkMLSchema = SchemaDefinition

type LinkMLClassName = str
type LinkMLSlotOwner = ClassDefinition

LinkMLPrimitiveType = NewType("LinkMLPrimitiveType", str)
