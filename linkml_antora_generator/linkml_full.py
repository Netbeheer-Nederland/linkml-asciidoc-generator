from __future__ import annotations

from datetime import (
    datetime,
)
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    PrivateAttr,
)


metamodel_version = "1.8.0"  # LinkML Schema metamodel version."
version = "1.8.4"  # LinkML Pydantic generator version,


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )

    _meta: dict = PrivateAttr(default_factory=dict)


class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = None


class PvFormulaOptions(str, Enum):
    """
    The formula used to generate the set of permissible values from the code_set values
    """

    # The permissible values are the set of possible codes in the code set
    CODE = "CODE"
    # The permissible values are the set of CURIES in the code set
    CURIE = "CURIE"
    # The permissible values are the set of code URIs in the code set
    URI = "URI"
    # The permissible values are the set of FHIR coding elements derived from the code set
    FHIR_CODING = "FHIR_CODING"
    # The permissible values are the set of human readable labels in the code set
    LABEL = "LABEL"


class PresenceEnum(str, Enum):
    """
    enumeration of conditions by which a slot value should be set
    """

    UNCOMMITTED = "UNCOMMITTED"
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"


class RelationalRoleEnum(str, Enum):
    """
    enumeration of roles a slot on a relationship class can play
    """

    # a slot with this role connects a relationship to its subject/source node
    SUBJECT = "SUBJECT"
    # a slot with this role connects a relationship to its object/target node
    OBJECT = "OBJECT"
    # a slot with this role connects a relationship to its predicate/property
    PREDICATE = "PREDICATE"
    # a slot with this role connects a symmetric relationship to a node that represents either subject or object node
    NODE = "NODE"
    # a slot with this role connects a relationship to a node that is not subject/object/predicate
    OTHER_ROLE = "OTHER_ROLE"


class AliasPredicateEnum(str, Enum):
    """
    permissible values for the relationship between an element and an alias
    """

    EXACT_SYNONYM = "EXACT_SYNONYM"
    RELATED_SYNONYM = "RELATED_SYNONYM"
    BROAD_SYNONYM = "BROAD_SYNONYM"
    NARROW_SYNONYM = "NARROW_SYNONYM"


class ObligationLevelEnum(str, Enum):
    """
    The level of obligation or recommendation strength for a metadata element
    """

    # The metadata element is required to be present in the model
    REQUIRED = "REQUIRED"
    # The metadata element is recommended to be present in the model
    RECOMMENDED = "RECOMMENDED"
    # The metadata element is optional to be present in the model
    OPTIONAL = "OPTIONAL"
    # The metadata element is an example of how to use the model
    EXAMPLE = "EXAMPLE"
    # The metadata element is allowed but discouraged to be present in the model
    DISCOURAGED = "DISCOURAGED"


class Extension(ConfiguredBaseModel):
    """
    a tag/value pair used to add non-model information to an entry
    """

    tag: str = Field(..., description="""a tag associated with an extension""")
    value: Any = Field(..., description="""the actual annotation""")
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )


class Extensible(ConfiguredBaseModel):
    """
    mixin for classes that support extension
    """

    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )


class Annotatable(ConfiguredBaseModel):
    """
    mixin for classes that support annotations
    """

    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )


# class Annotation(Annotatable, Extension):
#     """
#     a tag/value pair with the semantics of OWL Annotation
#     """
#     # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
#     annotations: Optional[Dict[str, str]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
#     tag: str = Field(..., description="""a tag associated with an extension""")
#     value: Any = Field(..., description="""the actual annotation""")
#     extensions: Optional[Dict[str, Extension]] = Field(None, description="""a tag/text tuple attached to an arbitrary element""")


class UnitOfMeasure(ConfiguredBaseModel):
    """
    A unit of measure, or unit, is a particular quantity value that has been chosen as a scale for  measuring other quantities the same kind (more generally of equivalent dimension).
    """

    symbol: Optional[str] = Field(
        None, description="""name of the unit encoded as a symbol"""
    )
    abbreviation: Optional[str] = Field(
        None,
        description="""An abbreviation for a unit is a short ASCII string that is used in place of the full name for the unit in  contexts where non-ASCII characters would be problematic, or where using the abbreviation will enhance  readability. When a power of a base unit needs to be expressed, such as squares this can be done using  abbreviations rather than symbols (source: qudt)""",
    )
    descriptive_name: Optional[str] = Field(
        None,
        description="""the spelled out name of the unit, for example, meter""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""Used to link a unit to equivalent concepts in ontologies such as UO, SNOMED, OEM, OBOE, NCIT""",
    )
    ucum_code: Optional[str] = Field(
        None,
        description="""associates a QUDT unit with its UCUM code (case-sensitive).""",
    )
    derivation: Optional[str] = Field(
        None,
        description="""Expression for deriving this unit from other units""",
    )
    has_quantity_kind: Optional[str] = Field(
        None,
        description="""Concept in a vocabulary or ontology that denotes the kind of quantity being measured, e.g. length""",
    )
    iec61360code: Optional[str] = Field(None)


class CommonMetadata(ConfiguredBaseModel):
    """
    Generic metadata shared across definitions
    """

    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class Element(CommonMetadata, Annotatable, Extensible):
    """
    A named element in the model
    """

    # name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""")
    id_prefixes: Optional[List[str]] = Field(
        None,
        description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""",
    )
    id_prefixes_are_closed: Optional[bool] = Field(
        None,
        description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""",
    )
    definition_uri: Optional[str] = Field(
        None,
        description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""",
    )
    local_names: Optional[Dict[str, Union[str, LocalName]]] = Field(None)
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class SchemaDefinition(Element):
    """
    A collection of definitions that make up a schema or a data model.
    """

    id: str = Field(..., description="""The official schema URI""")
    version: Optional[str] = Field(
        None, description="""particular version of schema"""
    )
    imports: Optional[List[str]] = Field(
        None,
        description="""A list of schemas that are to be included in this schema""",
    )
    license: Optional[str] = Field(
        None, description="""license for the schema"""
    )
    # prefixes: Optional[Dict[str, Union[str, Prefix]]] = Field(None, description="""A collection of prefix expansions that specify how CURIEs can be expanded to URIs""")
    prefixes: Optional[Dict[str, str]] = Field(
        None,
        description="""A collection of prefix expansions that specify how CURIEs can be expanded to URIs""",
    )
    emit_prefixes: Optional[List[str]] = Field(
        None,
        description="""a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.""",
    )
    default_curi_maps: Optional[List[str]] = Field(
        None,
        description="""ordered list of prefixcommon biocontexts to be fetched to resolve id prefixes and inline prefix variables""",
    )
    default_prefix: Optional[str] = Field(
        None,
        description="""The prefix that is used for all elements within a schema""",
    )
    default_range: Optional[str] = Field(
        None,
        description="""default slot range to be used if range element is omitted from a slot definition""",
    )
    subsets: Optional[Dict[str, SubsetDefinition]] = Field(
        None,
        description="""An index to the collection of all subset definitions in the schema""",
    )
    types: Optional[Dict[str, TypeDefinition]] = Field(
        None,
        description="""An index to the collection of all type definitions in the schema""",
    )
    enums: Optional[Dict[str, EnumDefinition]] = Field(
        None,
        description="""An index to the collection of all enum definitions in the schema""",
    )
    slots: Optional[Dict[str, SlotDefinition]] = Field(
        None,
        description="""An index to the collection of all slot definitions in the schema""",
    )
    classes: Optional[Dict[str, ClassDefinition]] = Field(
        None,
        description="""An index to the collection of all class definitions in the schema""",
    )
    metamodel_version: Optional[str] = Field(
        None,
        description="""Version of the metamodel used to load the schema""",
    )
    source_file: Optional[str] = Field(
        None,
        description="""name, uri or description of the source of the schema""",
    )
    source_file_date: Optional[datetime] = Field(
        None, description="""modification date of the source of the schema"""
    )
    source_file_size: Optional[int] = Field(
        None, description="""size in bytes of the source of the schema"""
    )
    generation_date: Optional[datetime] = Field(
        None,
        description="""date and time that the schema was loaded/generated""",
    )
    slot_names_unique: Optional[bool] = Field(
        None,
        description="""if true then induced/mangled slot names are not created for class_usage and attributes""",
    )
    settings: Optional[Dict[str, Union[str, Setting]]] = Field(
        None, description="""A collection of global variable settings"""
    )
    bindings: Optional[List[EnumBinding]] = Field(
        None,
        description="""A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.""",
    )
    name: str = Field(
        ...,
        description="""a unique name for the schema that is both human-readable and consists of only characters from the NCName set""",
    )
    id_prefixes: Optional[List[str]] = Field(
        None,
        description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""",
    )
    id_prefixes_are_closed: Optional[bool] = Field(
        None,
        description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""",
    )
    definition_uri: Optional[str] = Field(
        None,
        description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""",
    )
    local_names: Optional[Dict[str, Union[str, LocalName]]] = Field(None)
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class SubsetDefinition(Element):
    """
    an element that can be used to group other metamodel elements
    """

    # name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""")
    id_prefixes: Optional[List[str]] = Field(
        None,
        description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""",
    )
    id_prefixes_are_closed: Optional[bool] = Field(
        None,
        description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""",
    )
    definition_uri: Optional[str] = Field(
        None,
        description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""",
    )
    local_names: Optional[Dict[str, Union[str, LocalName]]] = Field(None)
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class Definition(Element):
    """
    abstract base class for core metaclasses
    """

    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""",
    )
    abstract: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""",
    )
    mixin: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""",
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""",
    )
    apply_to: Optional[List[str]] = Field(
        None,
        description="""Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.""",
    )
    values_from: Optional[List[str]] = Field(
        None,
        description="""The identifier of a \"value set\" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""",
    )
    string_serialization: Optional[str] = Field(
        None,
        description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""",
    )
    # name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""")
    id_prefixes: Optional[List[str]] = Field(
        None,
        description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""",
    )
    id_prefixes_are_closed: Optional[bool] = Field(
        None,
        description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""",
    )
    definition_uri: Optional[str] = Field(
        None,
        description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""",
    )
    local_names: Optional[Dict[str, Union[str, LocalName]]] = Field(None)
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class EnumBinding(CommonMetadata, Annotatable, Extensible):
    """
    A binding of a slot or a class to a permissible value from an enumeration.
    """

    range: Optional[str] = Field(
        None,
        description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""",
    )
    obligation_level: Optional[ObligationLevelEnum] = Field(
        None,
        description="""The level of obligation or recommendation strength for a metadata element""",
    )
    binds_value_of: Optional[str] = Field(
        None,
        description="""A path to a slot that is being bound to a permissible value from an enumeration.""",
    )
    pv_formula: Optional[PvFormulaOptions] = Field(
        None,
        description="""Defines the specific formula to be used to generate the permissible values.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class MatchQuery(ConfiguredBaseModel):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissivle values via a query that  matches on properties of the external concepts.
    """

    identifier_pattern: Optional[str] = Field(
        None,
        description="""A regular expression that is used to obtain a set of identifiers from a source_ontology to construct a set of permissible values""",
    )
    source_ontology: Optional[str] = Field(
        None,
        description="""An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values""",
    )


class ReachabilityQuery(ConfiguredBaseModel):
    """
    A query that is used on an enum expression to dynamically obtain a set of permissible values via walking from a  set of source nodes to a set of descendants or ancestors over a set of relationship types.
    """

    source_ontology: Optional[str] = Field(
        None,
        description="""An ontology or vocabulary or terminology that is used in a query to obtain a set of permissible values""",
    )
    source_nodes: Optional[List[str]] = Field(
        None,
        description="""A list of nodes that are used in the reachability query""",
    )
    relationship_types: Optional[List[str]] = Field(
        None,
        description="""A list of relationship types (properties) that are used in a reachability query""",
    )
    is_direct: Optional[bool] = Field(
        None,
        description="""True if the reachability query should only include directly related nodes, if False then include also transitively connected""",
    )
    include_self: Optional[bool] = Field(
        None, description="""True if the query is reflexive"""
    )
    traverse_up: Optional[bool] = Field(
        None,
        description="""True if the direction of the reachability query is reversed and ancestors are retrieved""",
    )


class Expression(ConfiguredBaseModel):
    """
    general mixin for any class that can represent some form of expression
    """

    pass


class TypeExpression(Expression):
    """
    An abstract class grouping named types and anonymous type expressions
    """

    pattern: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string""",
    )
    structured_pattern: Optional[PatternExpression] = Field(
        None,
        description="""the string value of the slot must conform to the regular expression in the pattern expression""",
    )
    unit: Optional[UnitOfMeasure] = Field(
        None, description="""an encoding of a unit"""
    )
    implicit_prefix: Optional[str] = Field(
        None,
        description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""",
    )
    equals_string: Optional[str] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal the specified value""",
    )
    equals_string_in: Optional[List[str]] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal one of the specified values""",
    )
    equals_number: Optional[int] = Field(
        None,
        description="""the slot must have range of a number and the value of the slot must equal the specified value""",
    )
    minimum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or higher than this""",
    )
    maximum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or lower than this""",
    )
    none_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    any_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    all_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )


class AnonymousTypeExpression(TypeExpression):
    """
    A type expression that is not a top-level named type definition. Used for nesting.
    """

    pattern: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string""",
    )
    structured_pattern: Optional[PatternExpression] = Field(
        None,
        description="""the string value of the slot must conform to the regular expression in the pattern expression""",
    )
    unit: Optional[UnitOfMeasure] = Field(
        None, description="""an encoding of a unit"""
    )
    implicit_prefix: Optional[str] = Field(
        None,
        description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""",
    )
    equals_string: Optional[str] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal the specified value""",
    )
    equals_string_in: Optional[List[str]] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal one of the specified values""",
    )
    equals_number: Optional[int] = Field(
        None,
        description="""the slot must have range of a number and the value of the slot must equal the specified value""",
    )
    minimum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or higher than this""",
    )
    maximum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or lower than this""",
    )
    none_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    any_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    all_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )


class TypeDefinition(TypeExpression, Element):
    """
    an element that whose instances are atomic scalar values that can be mapped to primitive types
    """

    typeof: Optional[str] = Field(
        None,
        description="""A parent type from which type properties are inherited""",
    )
    base: Optional[str] = Field(
        None,
        description="""python base type in the LinkML runtime that implements this type definition""",
    )
    uri: Optional[str] = Field(
        None,
        description="""The uri that defines the possible values for the type definition""",
    )
    repr: Optional[str] = Field(
        None,
        description="""the name of the python object that implements this type definition""",
    )
    union_of: Optional[List[str]] = Field(
        None,
        description="""indicates that the domain element consists exactly of the members of the element in the range.""",
    )
    pattern: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string""",
    )
    structured_pattern: Optional[PatternExpression] = Field(
        None,
        description="""the string value of the slot must conform to the regular expression in the pattern expression""",
    )
    unit: Optional[UnitOfMeasure] = Field(
        None, description="""an encoding of a unit"""
    )
    implicit_prefix: Optional[str] = Field(
        None,
        description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""",
    )
    equals_string: Optional[str] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal the specified value""",
    )
    equals_string_in: Optional[List[str]] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal one of the specified values""",
    )
    equals_number: Optional[int] = Field(
        None,
        description="""the slot must have range of a number and the value of the slot must equal the specified value""",
    )
    minimum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or higher than this""",
    )
    maximum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or lower than this""",
    )
    none_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    any_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    all_of: Optional[List[AnonymousTypeExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )
    # name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""")
    id_prefixes: Optional[List[str]] = Field(
        None,
        description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""",
    )
    id_prefixes_are_closed: Optional[bool] = Field(
        None,
        description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""",
    )
    definition_uri: Optional[str] = Field(
        None,
        description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""",
    )
    local_names: Optional[Dict[str, Union[str, LocalName]]] = Field(None)
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class EnumExpression(Expression):
    """
    An expression that constrains the range of a slot
    """

    code_set: Optional[str] = Field(
        None, description="""the identifier of an enumeration code set."""
    )
    code_set_tag: Optional[str] = Field(
        None, description="""the version tag of the enumeration code set"""
    )
    code_set_version: Optional[str] = Field(
        None,
        description="""the version identifier of the enumeration code set""",
    )
    pv_formula: Optional[PvFormulaOptions] = Field(
        None,
        description="""Defines the specific formula to be used to generate the permissible values.""",
    )
    permissible_values: Optional[Dict[str, PermissibleValue]] = Field(
        None, description="""A list of possible values for a slot range"""
    )
    include: Optional[List[AnonymousEnumExpression]] = Field(
        None,
        description="""An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set""",
    )
    minus: Optional[List[AnonymousEnumExpression]] = Field(
        None,
        description="""An enum expression that yields a list of permissible values that are to be subtracted from the enum""",
    )
    inherits: Optional[List[str]] = Field(
        None,
        description="""An enum definition that is used as the basis to create a new enum""",
    )
    reachable_from: Optional[ReachabilityQuery] = Field(
        None,
        description="""Specifies a query for obtaining a list of permissible values based on graph reachability""",
    )
    matches: Optional[MatchQuery] = Field(
        None,
        description="""Specifies a match query that is used to calculate the list of permissible values""",
    )
    concepts: Optional[List[str]] = Field(
        None,
        description="""A list of identifiers that are used to construct a set of permissible values""",
    )


class AnonymousEnumExpression(EnumExpression):
    """
    An enum_expression that is not named
    """

    code_set: Optional[str] = Field(
        None, description="""the identifier of an enumeration code set."""
    )
    code_set_tag: Optional[str] = Field(
        None, description="""the version tag of the enumeration code set"""
    )
    code_set_version: Optional[str] = Field(
        None,
        description="""the version identifier of the enumeration code set""",
    )
    pv_formula: Optional[PvFormulaOptions] = Field(
        None,
        description="""Defines the specific formula to be used to generate the permissible values.""",
    )
    permissible_values: Optional[Dict[str, PermissibleValue]] = Field(
        None, description="""A list of possible values for a slot range"""
    )
    include: Optional[List[AnonymousEnumExpression]] = Field(
        None,
        description="""An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set""",
    )
    minus: Optional[List[AnonymousEnumExpression]] = Field(
        None,
        description="""An enum expression that yields a list of permissible values that are to be subtracted from the enum""",
    )
    inherits: Optional[List[str]] = Field(
        None,
        description="""An enum definition that is used as the basis to create a new enum""",
    )
    reachable_from: Optional[ReachabilityQuery] = Field(
        None,
        description="""Specifies a query for obtaining a list of permissible values based on graph reachability""",
    )
    matches: Optional[MatchQuery] = Field(
        None,
        description="""Specifies a match query that is used to calculate the list of permissible values""",
    )
    concepts: Optional[List[str]] = Field(
        None,
        description="""A list of identifiers that are used to construct a set of permissible values""",
    )


class EnumDefinition(EnumExpression, Definition):
    """
    an element whose instances must be drawn from a specified set of permissible values
    """

    enum_uri: Optional[str] = Field(
        None,
        description="""URI of the enum that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas""",
    )
    code_set: Optional[str] = Field(
        None, description="""the identifier of an enumeration code set."""
    )
    code_set_tag: Optional[str] = Field(
        None, description="""the version tag of the enumeration code set"""
    )
    code_set_version: Optional[str] = Field(
        None,
        description="""the version identifier of the enumeration code set""",
    )
    pv_formula: Optional[PvFormulaOptions] = Field(
        None,
        description="""Defines the specific formula to be used to generate the permissible values.""",
    )
    permissible_values: Optional[Dict[str, PermissibleValue]] = Field(
        None, description="""A list of possible values for a slot range"""
    )
    include: Optional[List[AnonymousEnumExpression]] = Field(
        None,
        description="""An enum expression that yields a list of permissible values that are to be included, after subtracting the minus set""",
    )
    minus: Optional[List[AnonymousEnumExpression]] = Field(
        None,
        description="""An enum expression that yields a list of permissible values that are to be subtracted from the enum""",
    )
    inherits: Optional[List[str]] = Field(
        None,
        description="""An enum definition that is used as the basis to create a new enum""",
    )
    reachable_from: Optional[ReachabilityQuery] = Field(
        None,
        description="""Specifies a query for obtaining a list of permissible values based on graph reachability""",
    )
    matches: Optional[MatchQuery] = Field(
        None,
        description="""Specifies a match query that is used to calculate the list of permissible values""",
    )
    concepts: Optional[List[str]] = Field(
        None,
        description="""A list of identifiers that are used to construct a set of permissible values""",
    )
    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""",
    )
    abstract: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""",
    )
    mixin: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""",
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""",
    )
    apply_to: Optional[List[str]] = Field(
        None,
        description="""Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.""",
    )
    values_from: Optional[List[str]] = Field(
        None,
        description="""The identifier of a \"value set\" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""",
    )
    string_serialization: Optional[str] = Field(
        None,
        description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""",
    )
    # name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""")
    id_prefixes: Optional[List[str]] = Field(
        None,
        description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""",
    )
    id_prefixes_are_closed: Optional[bool] = Field(
        None,
        description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""",
    )
    definition_uri: Optional[str] = Field(
        None,
        description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""",
    )
    local_names: Optional[Dict[str, Union[str, LocalName]]] = Field(None)
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class StructuredAlias(Expression, CommonMetadata, Annotatable, Extensible):
    """
    object that contains meta data about a synonym or alias including where it came from (source) and its scope (narrow, broad, etc.)
    """

    literal_form: str = Field(
        ...,
        description="""The literal lexical form of a structured alias; i.e the actual alias value.""",
    )
    predicate: Optional[AliasPredicateEnum] = Field(
        None,
        description="""The relationship between an element and its alias.""",
    )
    categories: Optional[List[str]] = Field(
        None,
        description="""The category or categories of an alias. This can be drawn from any relevant vocabulary""",
    )
    contexts: Optional[List[str]] = Field(
        None, description="""The context in which an alias should be applied"""
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class AnonymousExpression(Expression, CommonMetadata, Annotatable, Extensible):
    """
    An abstract parent class for any nested expression
    """

    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class PathExpression(Expression, CommonMetadata, Annotatable, Extensible):
    """
    An expression that describes an abstract path from an object to another through a sequence of slot lookups
    """

    followed_by: Optional[PathExpression] = Field(
        None,
        description="""in a sequential list, this indicates the next member""",
    )
    none_of: Optional[List[PathExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    any_of: Optional[List[PathExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    all_of: Optional[List[PathExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )
    exactly_one_of: Optional[List[PathExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    reversed: Optional[bool] = Field(
        None, description="""true if the slot is to be inversed"""
    )
    traverse: Optional[str] = Field(
        None, description="""the slot to traverse"""
    )
    range_expression: Optional[AnonymousClassExpression] = Field(
        None,
        description="""A range that is described as a boolean expression combining existing ranges""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class SlotExpression(Expression):
    """
    an expression that constrains the range of values a slot can take
    """

    range: Optional[str] = Field(
        None,
        description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""",
    )
    range_expression: Optional[AnonymousClassExpression] = Field(
        None,
        description="""A range that is described as a boolean expression combining existing ranges""",
    )
    enum_range: Optional[EnumExpression] = Field(
        None, description="""An inlined enumeration"""
    )
    bindings: Optional[List[EnumBinding]] = Field(
        None,
        description="""A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.""",
    )
    required: Optional[bool] = Field(
        None,
        description="""true means that the slot must be present in instances of the class definition""",
    )
    recommended: Optional[bool] = Field(
        None,
        description="""true means that the slot should be present in instances of the class definition, but this is not required""",
    )
    multivalued: Optional[bool] = Field(
        None,
        description="""true means that slot can have more than one value and should be represented using a list or collection structure.""",
    )
    inlined: Optional[bool] = Field(
        None,
        description="""True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.""",
    )
    inlined_as_list: Optional[bool] = Field(
        None,
        description="""True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.""",
    )
    minimum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or higher than this""",
    )
    maximum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or lower than this""",
    )
    pattern: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string""",
    )
    structured_pattern: Optional[PatternExpression] = Field(
        None,
        description="""the string value of the slot must conform to the regular expression in the pattern expression""",
    )
    unit: Optional[UnitOfMeasure] = Field(
        None, description="""an encoding of a unit"""
    )
    implicit_prefix: Optional[str] = Field(
        None,
        description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""",
    )
    value_presence: Optional[PresenceEnum] = Field(
        None,
        description="""if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)""",
    )
    equals_string: Optional[str] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal the specified value""",
    )
    equals_string_in: Optional[List[str]] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal one of the specified values""",
    )
    equals_number: Optional[int] = Field(
        None,
        description="""the slot must have range of a number and the value of the slot must equal the specified value""",
    )
    equals_expression: Optional[str] = Field(
        None,
        description="""the value of the slot must equal the value of the evaluated expression""",
    )
    exact_cardinality: Optional[int] = Field(
        None,
        description="""the exact number of entries for a multivalued slot""",
    )
    minimum_cardinality: Optional[int] = Field(
        None,
        description="""the minimum number of entries for a multivalued slot""",
    )
    maximum_cardinality: Optional[int] = Field(
        None,
        description="""the maximum number of entries for a multivalued slot""",
    )
    has_member: Optional[AnonymousSlotExpression] = Field(
        None,
        description="""the value of the slot is multivalued with at least one member satisfying the condition""",
    )
    all_members: Optional[AnonymousSlotExpression] = Field(
        None,
        description="""the value of the slot is multivalued with all members satisfying the condition""",
    )
    none_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    any_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    all_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )


class AnonymousSlotExpression(SlotExpression, AnonymousExpression):
    range: Optional[str] = Field(
        None,
        description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""",
    )
    range_expression: Optional[AnonymousClassExpression] = Field(
        None,
        description="""A range that is described as a boolean expression combining existing ranges""",
    )
    enum_range: Optional[EnumExpression] = Field(
        None, description="""An inlined enumeration"""
    )
    bindings: Optional[List[EnumBinding]] = Field(
        None,
        description="""A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.""",
    )
    required: Optional[bool] = Field(
        None,
        description="""true means that the slot must be present in instances of the class definition""",
    )
    recommended: Optional[bool] = Field(
        None,
        description="""true means that the slot should be present in instances of the class definition, but this is not required""",
    )
    multivalued: Optional[bool] = Field(
        None,
        description="""true means that slot can have more than one value and should be represented using a list or collection structure.""",
    )
    inlined: Optional[bool] = Field(
        None,
        description="""True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.""",
    )
    inlined_as_list: Optional[bool] = Field(
        None,
        description="""True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.""",
    )
    minimum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or higher than this""",
    )
    maximum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or lower than this""",
    )
    pattern: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string""",
    )
    structured_pattern: Optional[PatternExpression] = Field(
        None,
        description="""the string value of the slot must conform to the regular expression in the pattern expression""",
    )
    unit: Optional[UnitOfMeasure] = Field(
        None, description="""an encoding of a unit"""
    )
    implicit_prefix: Optional[str] = Field(
        None,
        description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""",
    )
    value_presence: Optional[PresenceEnum] = Field(
        None,
        description="""if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)""",
    )
    equals_string: Optional[str] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal the specified value""",
    )
    equals_string_in: Optional[List[str]] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal one of the specified values""",
    )
    equals_number: Optional[int] = Field(
        None,
        description="""the slot must have range of a number and the value of the slot must equal the specified value""",
    )
    equals_expression: Optional[str] = Field(
        None,
        description="""the value of the slot must equal the value of the evaluated expression""",
    )
    exact_cardinality: Optional[int] = Field(
        None,
        description="""the exact number of entries for a multivalued slot""",
    )
    minimum_cardinality: Optional[int] = Field(
        None,
        description="""the minimum number of entries for a multivalued slot""",
    )
    maximum_cardinality: Optional[int] = Field(
        None,
        description="""the maximum number of entries for a multivalued slot""",
    )
    has_member: Optional[AnonymousSlotExpression] = Field(
        None,
        description="""the value of the slot is multivalued with at least one member satisfying the condition""",
    )
    all_members: Optional[AnonymousSlotExpression] = Field(
        None,
        description="""the value of the slot is multivalued with all members satisfying the condition""",
    )
    none_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    any_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    all_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class SlotDefinition(SlotExpression, Definition):
    """
    an element that describes how instances are related to other instances
    """

    singular_name: Optional[str] = Field(
        None, description="""a name that is used in the singular form"""
    )
    domain: Optional[str] = Field(
        None,
        description="""defines the type of the subject of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts that X is an instance of C1
""",
    )
    slot_uri: Optional[str] = Field(
        None,
        description="""URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.""",
    )
    array: Optional[ArrayExpression] = Field(
        None,
        description="""coerces the value of the slot into an array and defines the dimensions of that array""",
    )
    inherited: Optional[bool] = Field(
        None,
        description="""true means that the *value* of a slot is inherited by subclasses""",
    )
    readonly: Optional[str] = Field(
        None,
        description="""If present, slot is read only.  Text explains why""",
    )
    ifabsent: Optional[str] = Field(
        None,
        description="""function that provides a default value for the slot.
  * [Tt]rue -- boolean True
  * [Ff]alse -- boolean False
  * bnode -- blank node identifier
  * class_curie -- CURIE for the containing class
  * class_uri -- URI for the containing class
  * default_ns -- schema default namespace
  * default_range -- schema default range
  * int(value) -- integer value
  * slot_uri -- URI for the slot
  * slot_curie -- CURIE for the slot
  * string(value) -- string value
  * EnumName(PermissibleValue) -- enum value""",
    )
    list_elements_unique: Optional[bool] = Field(
        None,
        description="""If True, then there must be no duplicates in the elements of a multivalued slot""",
    )
    list_elements_ordered: Optional[bool] = Field(
        None,
        description="""If True, then the order of elements of a multivalued slot is guaranteed to be preserved. If False, the order may still be preserved but this is not guaranteed""",
    )
    shared: Optional[bool] = Field(
        None,
        description="""If True, then the relationship between the slot domain and range is many to one or many to many""",
    )
    key: Optional[bool] = Field(
        None,
        description="""True means that the key slot(s) uniquely identify the elements within a single container""",
    )
    identifier: Optional[bool] = Field(
        None,
        description="""True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container""",
    )
    designates_type: Optional[bool] = Field(
        None,
        description="""True means that the key slot(s) is used to determine the instantiation (types) relation between objects and a ClassDefinition""",
    )
    alias: Optional[str] = Field(
        None,
        description="""the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.""",
    )
    owner: Optional[str] = Field(
        None,
        description="""the \"owner\" of the slot. It is the class if it appears in the slots list, otherwise the declaring slot""",
    )
    domain_of: Optional[List[str]] = Field(
        None,
        description="""the class(es) that reference the slot in a \"slots\" or \"slot_usage\" context""",
    )
    subproperty_of: Optional[str] = Field(
        None,
        description="""Ontology property which this slot is a subproperty of.  Note: setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""",
    )
    symmetric: Optional[bool] = Field(
        None, description="""If s is symmetric, and i.s=v, then v.s=i"""
    )
    reflexive: Optional[bool] = Field(
        None,
        description="""If s is reflexive, then i.s=i for all instances i""",
    )
    locally_reflexive: Optional[bool] = Field(
        None,
        description="""If s is locally_reflexive, then i.s=i for all instances i where s is a class slot for the type of i""",
    )
    irreflexive: Optional[bool] = Field(
        None,
        description="""If s is irreflexive, then there exists no i such i.s=i""",
    )
    asymmetric: Optional[bool] = Field(
        None,
        description="""If s is antisymmetric, and i.s=v where i is different from v, v.s cannot have value i""",
    )
    transitive: Optional[bool] = Field(
        None,
        description="""If s is transitive, and i.s=z, and s.s=j, then i.s=j""",
    )
    inverse: Optional[str] = Field(
        None,
        description="""indicates that any instance of d s r implies that there is also an instance of r s' d""",
    )
    is_class_field: Optional[bool] = Field(
        None,
        description="""indicates that for any instance, i, the domain of this slot will include an assertion of i s range""",
    )
    transitive_form_of: Optional[str] = Field(
        None,
        description="""If s transitive_form_of d, then (1) s holds whenever d holds (2) s is transitive (3) d holds whenever s holds and there are no intermediates, and s is not reflexive""",
    )
    reflexive_transitive_form_of: Optional[str] = Field(
        None, description="""transitive_form_of including the reflexive case"""
    )
    role: Optional[str] = Field(
        None,
        description="""a textual descriptor that indicates the role played by the slot range""",
    )
    is_usage_slot: Optional[bool] = Field(
        None,
        description="""True means that this slot was defined in a slot_usage situation""",
    )
    usage_slot_name: Optional[str] = Field(
        None,
        description="""The name of the slot referenced in the slot_usage""",
    )
    relational_role: Optional[RelationalRoleEnum] = Field(
        None,
        description="""the role a slot on a relationship class plays, for example, the subject, object or predicate roles""",
    )
    slot_group: Optional[str] = Field(
        None,
        description="""allows for grouping of related slots into a grouping slot that serves the role of a group""",
    )
    is_grouping_slot: Optional[bool] = Field(
        None, description="""true if this slot is a grouping slot"""
    )
    path_rule: Optional[PathExpression] = Field(
        None,
        description="""a rule for inferring a slot assignment based on evaluating a path through a sequence of slot assignments""",
    )
    disjoint_with: Optional[List[str]] = Field(
        None,
        description="""Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances""",
    )
    children_are_mutually_disjoint: Optional[bool] = Field(
        None,
        description="""If true then all direct is_a children are mutually disjoint and share no instances in common""",
    )
    union_of: Optional[List[str]] = Field(
        None,
        description="""indicates that the domain element consists exactly of the members of the element in the range.""",
    )
    type_mappings: Optional[List[str]] = Field(
        None,
        description="""A collection of type mappings that specify how a slot's range should be mapped or serialized in different frameworks""",
    )
    range: Optional[str] = Field(
        None,
        description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""",
    )
    range_expression: Optional[AnonymousClassExpression] = Field(
        None,
        description="""A range that is described as a boolean expression combining existing ranges""",
    )
    enum_range: Optional[EnumExpression] = Field(
        None, description="""An inlined enumeration"""
    )
    bindings: Optional[List[EnumBinding]] = Field(
        None,
        description="""A collection of enum bindings that specify how a slot can be bound to a permissible value from an enumeration.
LinkML provides enums to allow string values to be restricted to one of a set of permissible values (specified statically or dynamically).
Enum bindings allow enums to be bound to any object, including complex nested objects. For example, given a (generic) class Concept with slots id and label, it may be desirable to restrict the values the id takes on in a given context. For example, a HumanSample class may have a slot for representing sample site, with a range of concept, but the values of that slot may be restricted to concepts from a particular branch of an anatomy ontology.""",
    )
    required: Optional[bool] = Field(
        None,
        description="""true means that the slot must be present in instances of the class definition""",
    )
    recommended: Optional[bool] = Field(
        None,
        description="""true means that the slot should be present in instances of the class definition, but this is not required""",
    )
    multivalued: Optional[bool] = Field(
        None,
        description="""true means that slot can have more than one value and should be represented using a list or collection structure.""",
    )
    inlined: Optional[bool] = Field(
        None,
        description="""True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.""",
    )
    inlined_as_list: Optional[bool] = Field(
        None,
        description="""True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.""",
    )
    minimum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or higher than this""",
    )
    maximum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or lower than this""",
    )
    pattern: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string""",
    )
    structured_pattern: Optional[PatternExpression] = Field(
        None,
        description="""the string value of the slot must conform to the regular expression in the pattern expression""",
    )
    unit: Optional[UnitOfMeasure] = Field(
        None, description="""an encoding of a unit"""
    )
    implicit_prefix: Optional[str] = Field(
        None,
        description="""Causes the slot value to be interpreted as a uriorcurie after prefixing with this string""",
    )
    value_presence: Optional[PresenceEnum] = Field(
        None,
        description="""if PRESENT then a value must be present (for lists there must be at least one value). If ABSENT then a value must be absent (for lists, must be empty)""",
    )
    equals_string: Optional[str] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal the specified value""",
    )
    equals_string_in: Optional[List[str]] = Field(
        None,
        description="""the slot must have range string and the value of the slot must equal one of the specified values""",
    )
    equals_number: Optional[int] = Field(
        None,
        description="""the slot must have range of a number and the value of the slot must equal the specified value""",
    )
    equals_expression: Optional[str] = Field(
        None,
        description="""the value of the slot must equal the value of the evaluated expression""",
    )
    exact_cardinality: Optional[int] = Field(
        None,
        description="""the exact number of entries for a multivalued slot""",
    )
    minimum_cardinality: Optional[int] = Field(
        None,
        description="""the minimum number of entries for a multivalued slot""",
    )
    maximum_cardinality: Optional[int] = Field(
        None,
        description="""the maximum number of entries for a multivalued slot""",
    )
    has_member: Optional[AnonymousSlotExpression] = Field(
        None,
        description="""the value of the slot is multivalued with at least one member satisfying the condition""",
    )
    all_members: Optional[AnonymousSlotExpression] = Field(
        None,
        description="""the value of the slot is multivalued with all members satisfying the condition""",
    )
    none_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    any_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    all_of: Optional[List[AnonymousSlotExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )
    is_a: Optional[str] = Field(
        None,
        description="""A primary parent slot from which inheritable metaslots are propagated""",
    )
    abstract: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""",
    )
    mixin: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""",
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent mixin slots from which inheritable metaslots are propagated""",
    )
    apply_to: Optional[List[str]] = Field(
        None,
        description="""Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.""",
    )
    values_from: Optional[List[str]] = Field(
        None,
        description="""The identifier of a \"value set\" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""",
    )
    string_serialization: Optional[str] = Field(
        None,
        description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""",
    )
    # name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""")
    id_prefixes: Optional[List[str]] = Field(
        None,
        description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""",
    )
    id_prefixes_are_closed: Optional[bool] = Field(
        None,
        description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""",
    )
    definition_uri: Optional[str] = Field(
        None,
        description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""",
    )
    local_names: Optional[Dict[str, Union[str, LocalName]]] = Field(None)
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class ClassExpression(ConfiguredBaseModel):
    """
    A boolean expression that can be used to dynamically determine membership of a class
    """

    any_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    none_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    all_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )
    slot_conditions: Optional[Dict[str, SlotDefinition]] = Field(
        None,
        description="""expresses constraints on a group of slots for a class expression""",
    )


class AnonymousClassExpression(ClassExpression, AnonymousExpression):
    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""",
    )
    any_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    none_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    all_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )
    slot_conditions: Optional[Dict[str, SlotDefinition]] = Field(
        None,
        description="""expresses constraints on a group of slots for a class expression""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class ClassDefinition(ClassExpression, Definition):
    """
    an element whose instances are complex objects that may have slot-value assignments
    """

    slots: Optional[List[str]] = Field(
        None,
        description="""collection of slot names that are applicable to a class""",
    )
    slot_usage: Optional[Dict[str, SlotDefinition]] = Field(
        None,
        description="""the refinement of a slot in the context of the containing class definition.""",
    )
    attributes: Optional[Dict[str, SlotDefinition]] = Field(
        None, description="""Inline definition of slots"""
    )
    class_uri: Optional[str] = Field(
        None,
        description="""URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas""",
    )
    subclass_of: Optional[str] = Field(
        None,
        description="""DEPRECATED -- rdfs:subClassOf to be emitted in OWL generation""",
    )
    union_of: Optional[List[str]] = Field(
        None,
        description="""indicates that the domain element consists exactly of the members of the element in the range.""",
    )
    defining_slots: Optional[List[str]] = Field(
        None,
        description="""The combination of is a plus defining slots form a genus-differentia definition, or the set of necessary and sufficient conditions that can be transformed into an OWL equivalence axiom""",
    )
    tree_root: Optional[bool] = Field(
        None,
        description="""Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations""",
    )
    unique_keys: Optional[Dict[str, UniqueKey]] = Field(
        None,
        description="""A collection of named unique keys for this class. Unique keys may be singular or compound.""",
    )
    rules: Optional[List[ClassRule]] = Field(
        None,
        description="""the collection of rules that apply to all members of this class""",
    )
    classification_rules: Optional[List[AnonymousClassExpression]] = Field(
        None,
        description="""The collection of classification rules that apply to all members of this class. Classification rules allow for automatically assigning the instantiated type of an instance.""",
    )
    slot_names_unique: Optional[bool] = Field(
        None,
        description="""if true then induced/mangled slot names are not created for class_usage and attributes""",
    )
    represents_relationship: Optional[bool] = Field(
        None,
        description="""true if this class represents a relationship rather than an entity""",
    )
    disjoint_with: Optional[List[str]] = Field(
        None,
        description="""Two classes are disjoint if they have no instances in common, two slots are disjoint if they can never hold between the same two instances""",
    )
    children_are_mutually_disjoint: Optional[bool] = Field(
        None,
        description="""If true then all direct is_a children are mutually disjoint and share no instances in common""",
    )
    any_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if at least one of the expressions hold"""
    )
    exactly_one_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if only one of the expressions hold"""
    )
    none_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if none of the expressions hold"""
    )
    all_of: Optional[List[AnonymousClassExpression]] = Field(
        None, description="""holds if all of the expressions hold"""
    )
    slot_conditions: Optional[Dict[str, SlotDefinition]] = Field(
        None,
        description="""expresses constraints on a group of slots for a class expression""",
    )
    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class from which inheritable metaslots are propagated""",
    )
    abstract: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""",
    )
    mixin: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""",
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent mixin classes from which inheritable metaslots are propagated""",
    )
    apply_to: Optional[List[str]] = Field(
        None,
        description="""Used to extend class or slot definitions. For example, if we have a core schema where a gene has two slots for identifier and symbol, and we have a specialized schema for my_organism where we wish to add a slot systematic_name, we can avoid subclassing by defining a class gene_my_organism, adding the slot to this class, and then adding an apply_to pointing to the gene class. The new slot will be 'injected into' the gene class.""",
    )
    values_from: Optional[List[str]] = Field(
        None,
        description="""The identifier of a \"value set\" -- a set of identifiers that form the possible values for the range of a slot. Note: this is different than 'subproperty_of' in that 'subproperty_of' is intended to be a single ontology term while 'values_from' is the identifier of an entire value set.  Additionally, this is different than an enumeration in that in an enumeration, the values of the enumeration are listed directly in the model itself. Setting this property on a slot does not guarantee an expansion of the ontological hierarchy into an enumerated list of possible values in every serialization of the model.""",
    )
    string_serialization: Optional[str] = Field(
        None,
        description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""",
    )
    # name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""")
    id_prefixes: Optional[List[str]] = Field(
        None,
        description="""An allowed list of prefixes for which identifiers must conform. The identifier of this class or slot must begin with the URIs referenced by this prefix""",
    )
    id_prefixes_are_closed: Optional[bool] = Field(
        None,
        description="""If true, then the id_prefixes slot is treated as being closed, and any use of an id that does not have this prefix is considered a violation.""",
    )
    definition_uri: Optional[str] = Field(
        None,
        description="""The native URI of the element. This is always within the namespace of the containing schema. Contrast with the assigned URI, via class_uri or slot_uri""",
    )
    local_names: Optional[Dict[str, Union[str, LocalName]]] = Field(None)
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class ClassLevelRule(ConfiguredBaseModel):
    """
    A rule that is applied to classes
    """

    pass


class ClassRule(ClassLevelRule, CommonMetadata, Annotatable, Extensible):
    """
    A rule that applies to instances of a class
    """

    preconditions: Optional[AnonymousClassExpression] = Field(
        None,
        description="""an expression that must hold in order for the rule to be applicable to an instance""",
    )
    postconditions: Optional[AnonymousClassExpression] = Field(
        None,
        description="""an expression that must hold for an instance of the class, if the preconditions hold""",
    )
    elseconditions: Optional[AnonymousClassExpression] = Field(
        None,
        description="""an expression that must hold for an instance of the class, if the preconditions no not hold""",
    )
    bidirectional: Optional[bool] = Field(
        None,
        description="""in addition to preconditions entailing postconditions, the postconditions entail the preconditions""",
    )
    open_world: Optional[bool] = Field(
        None,
        description="""if true, the the postconditions may be omitted in instance data, but it is valid for an inference engine to add these""",
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    deactivated: Optional[bool] = Field(
        None,
        description="""a deactivated rule is not executed by the rules engine""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class ArrayExpression(CommonMetadata, Annotatable, Extensible):
    """
    defines the dimensions of an array
    """

    exact_number_dimensions: Optional[int] = Field(
        None, description="""exact number of dimensions in the array"""
    )
    minimum_number_dimensions: Optional[int] = Field(
        None, description="""minimum number of dimensions in the array"""
    )
    maximum_number_dimensions: Optional[Union[bool, int]] = Field(
        None,
        description="""maximum number of dimensions in the array, or False if explicitly no maximum. If this is unset, and an explicit list of dimensions are passed using dimensions, then this is interpreted as a closed list and the maximum_number_dimensions is the length of the dimensions list, unless this value is set to False""",
    )
    dimensions: Optional[List[DimensionExpression]] = Field(
        None, description="""definitions of each axis in the array"""
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class DimensionExpression(CommonMetadata, Annotatable, Extensible):
    """
    defines one of the dimensions of an array
    """

    alias: Optional[str] = Field(
        None,
        description="""the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.""",
    )
    maximum_cardinality: Optional[int] = Field(
        None,
        description="""the maximum number of entries for a multivalued slot""",
    )
    minimum_cardinality: Optional[int] = Field(
        None,
        description="""the minimum number of entries for a multivalued slot""",
    )
    exact_cardinality: Optional[int] = Field(
        None,
        description="""the exact number of entries for a multivalued slot""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class PatternExpression(CommonMetadata, Annotatable, Extensible):
    """
    a regular expression pattern used to evaluate conformance of a string
    """

    syntax: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string. May be interpolated.""",
    )
    interpolated: Optional[bool] = Field(
        None,
        description="""if true then the pattern is first string interpolated""",
    )
    partial_match: Optional[bool] = Field(
        None,
        description="""if not true then the pattern must match the whole string, as if enclosed in ^...$""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class ImportExpression(CommonMetadata, Annotatable, Extensible):
    """
    an expression describing an import
    """

    import_from: str = Field(...)
    import_as: Optional[str] = Field(None)
    import_map: Optional[Dict[str, Union[str, Setting]]] = Field(None)
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class Setting(ConfiguredBaseModel):
    """
    assignment of a key to a value
    """

    setting_key: str = Field(
        ..., description="""the variable name for a setting"""
    )
    setting_value: str = Field(
        ..., description="""The value assigned for a setting"""
    )


# class Prefix(ConfiguredBaseModel):
#     """
#     prefix URI tuple
#     """
#     prefix_prefix: str = Field(..., description="""The prefix components of a prefix expansions. This is the part that appears before the colon in a CURIE.""")
#     prefix_reference: str = Field(..., description="""The namespace to which a prefix expands to.""")


class LocalName(ConfiguredBaseModel):
    """
    an attributed label
    """

    local_name_source: str = Field(
        ..., description="""the ncname of the source of the name"""
    )
    local_name_value: str = Field(
        ...,
        description="""a name assigned to an element in a given ontology""",
    )


class Example(ConfiguredBaseModel):
    """
    usage example and description
    """

    value: Optional[str] = Field(None, description="""example value""")
    description: Optional[str] = Field(
        None, description="""description of what the value is doing"""
    )
    object: Optional[Any] = Field(
        None, description="""direct object representation of the example"""
    )


class AltDescription(ConfiguredBaseModel):
    """
    an attributed description
    """

    source: str = Field(
        ..., description="""the source of an attributed description"""
    )
    description: str = Field(
        ..., description="""text of an attributed description"""
    )


class PermissibleValue(CommonMetadata, Annotatable, Extensible):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """

    # text: str = Field(..., description="""The actual permissible value itself""")
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    meaning: Optional[str] = Field(
        None, description="""the value meaning of a permissible value"""
    )
    unit: Optional[UnitOfMeasure] = Field(
        None, description="""an encoding of a unit"""
    )
    instantiates: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element instantiates.""",
    )
    implements: Optional[List[str]] = Field(
        None,
        description="""An element in another schema which this element conforms to. The referenced element is not imported into the schema for the implementing element. However, the referenced schema may be used to check conformance of the implementing element.""",
    )
    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""",
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class UniqueKey(CommonMetadata, Annotatable, Extensible):
    """
    a collection of slots whose values uniquely identify an instance of a class
    """

    unique_key_name: str = Field(..., description="""name of the unique key""")
    unique_key_slots: List[str] = Field(
        ...,
        description="""list of slot names that form a key. The tuple formed from the values of all these slots should be unique.""",
    )
    consider_nulls_inequal: Optional[bool] = Field(
        None,
        description="""By default, None values are considered equal for the purposes of comparisons in determining uniqueness. Set this to true to treat missing values as per ANSI-SQL NULLs, i.e NULL=NULL is always False.""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


class TypeMapping(CommonMetadata, Annotatable, Extensible):
    """
    Represents how a slot or type can be serialized to a format.
    """

    framework: str = Field(
        ...,
        description="""The name of a format that can be used to serialize LinkML data. The string value should be a code from the LinkML frameworks vocabulary, but this is not strictly enforced""",
    )
    type: Optional[str] = Field(None, description="""type to coerce to""")
    string_serialization: Optional[str] = Field(
        None,
        description="""Used on a slot that stores the string serialization of the containing object. The syntax follows python formatted strings, with slot names enclosed in {}s. These are expanded using the values of those slots.
We call the slot with the serialization the s-slot, the slots used in the {}s are v-slots. If both s-slots and v-slots are populated on an object then the value of the s-slot should correspond to the expansion.
Implementations of frameworks may choose to use this property to either (a) PARSE: implement automated normalizations by parsing denormalized strings into complex objects (b) GENERARE: implement automated to_string labeling of complex objects
For example, a Measurement class may have 3 fields: unit, value, and string_value. The string_value slot may have a string_serialization of {value}{unit} such that if unit=cm and value=2, the value of string_value shouldd be 2cm""",
    )
    extensions: Optional[Dict[str, Extension]] = Field(
        None,
        description="""a tag/text tuple attached to an arbitrary element""",
    )
    # annotations: Optional[Dict[str, Annotation]] = Field(None, description="""a collection of tag/text tuples with the semantics of OWL Annotation""")
    annotations: Optional[Dict[str, Any]] = Field(
        None,
        description="""a collection of tag/text tuples with the semantics of OWL Annotation""",
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
    )
    alt_descriptions: Optional[Dict[str, Union[str, AltDescription]]] = Field(
        None,
        description="""A sourced alternative description for an element""",
    )
    title: Optional[str] = Field(
        None,
        description="""A concise human-readable display label for the element. The title should mirror the name, and should use ordinary textual punctuation.""",
    )
    deprecated: Optional[str] = Field(
        None,
        description="""Description of why and when this element will no longer be used""",
    )
    todos: Optional[List[str]] = Field(
        None, description="""Outstanding issues that needs resolution"""
    )
    notes: Optional[List[str]] = Field(
        None,
        description="""editorial notes about an element intended primarily for internal consumption""",
    )
    comments: Optional[List[str]] = Field(
        None,
        description="""notes and comments about an element intended primarily for external consumption""",
    )
    examples: Optional[List[Example]] = Field(
        None, description="""example usages of an element"""
    )
    in_subset: Optional[List[str]] = Field(
        None,
        description="""used to indicate membership of a term in a defined subset of terms used for a particular domain or application.""",
    )
    from_schema: Optional[str] = Field(
        None, description="""id of the schema that defined the element"""
    )
    imported_from: Optional[str] = Field(
        None,
        description="""the imports entry that this element was derived from.  Empty means primary source""",
    )
    source: Optional[str] = Field(
        None,
        description="""A related resource from which the element is derived.""",
    )
    in_language: Optional[str] = Field(
        None, description="""the primary language used in the sources"""
    )
    see_also: Optional[List[str]] = Field(
        None,
        description="""A list of related entities or URLs that may be of relevance""",
    )
    deprecated_element_has_exact_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be automatically replaced by this uri or curie""",
    )
    deprecated_element_has_possible_replacement: Optional[str] = Field(
        None,
        description="""When an element is deprecated, it can be potentially replaced by this uri or curie""",
    )
    aliases: Optional[List[str]] = Field(
        None,
        description="""Alternate names/labels for the element. These do not alter the semantics of the schema, but may be useful to support search and alignment.""",
    )
    structured_aliases: Optional[List[StructuredAlias]] = Field(
        None,
        description="""A list of structured_alias objects, used to provide aliases in conjunction with additional metadata.""",
    )
    mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have comparable meaning. These may include terms that are precisely equivalent, broader or narrower in meaning, or otherwise semantically related but not equivalent from a strict ontological perspective.""",
    )
    exact_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have identical meaning.""",
    )
    close_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have close meaning.""",
    )
    related_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have related meaning.""",
    )
    narrow_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have narrower meaning.""",
    )
    broad_mappings: Optional[List[str]] = Field(
        None,
        description="""A list of terms from different schemas or terminology systems that have broader meaning.""",
    )
    created_by: Optional[str] = Field(
        None, description="""agent that created the element"""
    )
    contributors: Optional[List[str]] = Field(
        None, description="""agent that contributed to the element"""
    )
    created_on: Optional[datetime] = Field(
        None, description="""time at which the element was created"""
    )
    last_updated_on: Optional[datetime] = Field(
        None, description="""time at which the element was last updated"""
    )
    modified_by: Optional[str] = Field(
        None, description="""agent that modified the element"""
    )
    status: Optional[str] = Field(
        None, description="""status of the element"""
    )
    rank: Optional[int] = Field(
        None,
        description="""the relative order in which the element occurs, lower values are given precedence""",
    )
    categories: Optional[List[str]] = Field(
        None, description="""Controlled terms used to categorize an element."""
    )
    keywords: Optional[List[str]] = Field(
        None, description="""Keywords or tags used to describe the element"""
    )


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Extension.model_rebuild()
Extensible.model_rebuild()
Annotatable.model_rebuild()
# Annotation.model_rebuild()
UnitOfMeasure.model_rebuild()
CommonMetadata.model_rebuild()
Element.model_rebuild()
SchemaDefinition.model_rebuild()
SubsetDefinition.model_rebuild()
Definition.model_rebuild()
EnumBinding.model_rebuild()
MatchQuery.model_rebuild()
ReachabilityQuery.model_rebuild()
Expression.model_rebuild()
TypeExpression.model_rebuild()
AnonymousTypeExpression.model_rebuild()
TypeDefinition.model_rebuild()
EnumExpression.model_rebuild()
AnonymousEnumExpression.model_rebuild()
EnumDefinition.model_rebuild()
StructuredAlias.model_rebuild()
AnonymousExpression.model_rebuild()
PathExpression.model_rebuild()
SlotExpression.model_rebuild()
AnonymousSlotExpression.model_rebuild()
SlotDefinition.model_rebuild()
ClassExpression.model_rebuild()
AnonymousClassExpression.model_rebuild()
ClassDefinition.model_rebuild()
ClassLevelRule.model_rebuild()
ClassRule.model_rebuild()
ArrayExpression.model_rebuild()
DimensionExpression.model_rebuild()
PatternExpression.model_rebuild()
ImportExpression.model_rebuild()
Setting.model_rebuild()
# Prefix.model_rebuild()
LocalName.model_rebuild()
Example.model_rebuild()
AltDescription.model_rebuild()
PermissibleValue.model_rebuild()
UniqueKey.model_rebuild()
TypeMapping.model_rebuild()
