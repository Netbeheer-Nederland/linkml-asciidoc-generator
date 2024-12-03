from __future__ import annotations

import re
import sys
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar, Dict, List, Literal, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    PrivateAttr,
    field_validator,
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    pass


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


linkml_meta = LinkMLMeta(
    {
        "default_curi_maps": ["semweb_context"],
        "default_prefix": "linkml",
        "default_range": "string",
        "description": "A profile of the LinkML Schema metamodel to represent logical "
        "models in. The emphasis is on structural description and "
        "semantic alignment. Another aim is the avoidance of "
        "complicated and vague language semantics to improve ease of "
        "use and consistency in how schemas are interpreted, most "
        "notably by generators.",
        "emit_prefixes": [
            "linkml",
            "rdf",
            "rdfs",
            "xsd",
            "skos",
            "dcterms",
            "OIO",
            "owl",
            "pav",
        ],
        "id": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
        "imports": ["linkml:types"],
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "name": "linkml-prof-logical-model",
        "prefixes": {
            "IAO": {
                "prefix_prefix": "IAO",
                "prefix_reference": "http://purl.obolibrary.org/obo/IAO_",
            },
            "NCIT": {
                "prefix_prefix": "NCIT",
                "prefix_reference": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#",
            },
            "OIO": {
                "prefix_prefix": "OIO",
                "prefix_reference": "http://www.geneontology.org/formats/oboInOwl#",
            },
            "SIO": {
                "prefix_prefix": "SIO",
                "prefix_reference": "http://semanticscience.org/resource/SIO_",
            },
            "bibo": {
                "prefix_prefix": "bibo",
                "prefix_reference": "http://purl.org/ontology/bibo/",
            },
            "cdisc": {
                "prefix_prefix": "cdisc",
                "prefix_reference": "http://rdf.cdisc.org/mms#",
            },
            "linkml": {
                "prefix_prefix": "linkml",
                "prefix_reference": "https://w3id.org/linkml/",
            },
            "oslc": {
                "prefix_prefix": "oslc",
                "prefix_reference": "http://open-services.net/ns/core#",
            },
            "owl": {
                "prefix_prefix": "owl",
                "prefix_reference": "http://www.w3.org/2002/07/owl#",
            },
            "pav": {"prefix_prefix": "pav", "prefix_reference": "http://purl.org/pav/"},
            "prov": {
                "prefix_prefix": "prov",
                "prefix_reference": "http://www.w3.org/ns/prov#",
            },
            "qb": {
                "prefix_prefix": "qb",
                "prefix_reference": "http://purl.org/linked-data/cube#",
            },
            "qudt": {
                "prefix_prefix": "qudt",
                "prefix_reference": "http://qudt.org/schema/qudt/",
            },
            "schema": {
                "prefix_prefix": "schema",
                "prefix_reference": "http://schema.org/",
            },
            "sh": {
                "prefix_prefix": "sh",
                "prefix_reference": "http://www.w3.org/ns/shacl#",
            },
            "shex": {
                "prefix_prefix": "shex",
                "prefix_reference": "http://www.w3.org/ns/shex#",
            },
            "skos": {
                "prefix_prefix": "skos",
                "prefix_reference": "http://www.w3.org/2004/02/skos/core#",
            },
            "skosxl": {
                "prefix_prefix": "skosxl",
                "prefix_reference": "http://www.w3.org/2008/05/skos-xl#",
            },
            "swrl": {
                "prefix_prefix": "swrl",
                "prefix_reference": "http://www.w3.org/2003/11/swrl#",
            },
            "vann": {
                "prefix_prefix": "vann",
                "prefix_reference": "https://vocab.org/vann/",
            },
            "xsd": {
                "prefix_prefix": "xsd",
                "prefix_reference": "http://www.w3.org/2001/XMLSchema#",
            },
        },
        "source_file": "spec/meta.yaml",
        "title": "LinkML Schema Metamodel: `LogicalModel` Profile",
    }
)


class CommonMetadata(ConfiguredBaseModel):
    """
    Generic metadata shared across definitions
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "mixin": True,
        }
    )

    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )


class Expression(ConfiguredBaseModel):
    """
    general mixin for any class that can represent some form of expression
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "abstract": True,
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "mixin": True,
        }
    )

    pass


class Element(CommonMetadata):
    """
    A ndefault=amed element in the model
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "abstract": True,
            "aliases": ["data element", "object"],
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "mixins": ["common_metadata"],
            "see_also": ["https://en.wikipedia.org/wiki/Data_element"],
        }
    )

    _name: str = PrivateAttr(
        default=None
    )  # the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "conforms_to",
                "domain": "element",
                "domain_of": ["element"],
                "slot_uri": "dcterms:conformsTo",
            }
        },
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )


class Definition(Element):
    """
    abstract base class for core metaclasses
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "abstract": True,
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "see_also": ["https://en.wikipedia.org/wiki/Data_element_definition"],
        }
    )

    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""",
        json_schema_extra={
            "linkml_meta": {
                "abstract": True,
                "alias": "is_a",
                "domain_of": ["definition"],
                "rank": 11,
            }
        },
    )
    abstract: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "abstract",
                "domain": "definition",
                "domain_of": ["definition"],
            }
        },
    )
    mixin: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "mixin",
                "aliases": ["trait"],
                "domain": "definition",
                "domain_of": ["definition"],
                "see_also": ["https://en.wikipedia.org/wiki/Mixin"],
            }
        },
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "mixins",
                "aliases": ["traits"],
                "comments": [
                    "mixins act in the same way as parents (is_a). They allow a "
                    "model to have a primary strict hierarchy, while keeping the "
                    "benefits of multiple inheritance"
                ],
                "domain_of": ["definition"],
                "rank": 13,
                "see_also": ["https://en.wikipedia.org/wiki/Mixin"],
            }
        },
    )
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "conforms_to",
                "domain": "element",
                "domain_of": ["element"],
                "slot_uri": "dcterms:conformsTo",
            }
        },
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )


class SchemaDefinition(Element):
    """
    A collection of definitions that make up a schema or a data model.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": [
                "data dictionary",
                "data model",
                "information model",
                "logical model",
                "schema",
                "model",
            ],
            "close_mappings": ["qb:ComponentSet", "owl:Ontology"],
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "rank": 1,
            "see_also": ["https://en.wikipedia.org/wiki/Data_dictionary"],
            "slot_usage": {
                "name": {
                    "description": "a unique name for the schema that is "
                    "both human-readable and consists of "
                    "only characters from the NCName set",
                    "name": "name",
                    "range": "ncname",
                }
            },
            "tree_root": True,
        }
    )

    id: str = Field(
        ...,
        description="""The official schema URI""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "id",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "rank": 0,
            }
        },
    )
    version: Optional[str] = Field(
        None,
        description="""particular version of schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "version",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "exact_mappings": ["schema:schemaVersion"],
                "slot_uri": "pav:version",
            }
        },
    )
    license: Optional[str] = Field(
        None,
        description="""license for the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "license",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "rank": 31,
                "slot_uri": "dcterms:license",
            }
        },
    )
    prefixes: Optional[Dict[str, Union[str, Prefix]]] = Field(
        None,
        description="""A collection of prefix expansions that specify how CURIEs can be expanded to URIs""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefixes",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "rank": 10,
                "slot_uri": "sh:declare",
            }
        },
    )
    emit_prefixes: Optional[List[str]] = Field(
        None,
        description="""a list of Curie prefixes that are used in the representation of instances of the model.  All prefixes in this list are added to the prefix sections of the target models.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "emit_prefixes",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
            }
        },
    )
    default_prefix: Optional[str] = Field(
        None,
        description="""The prefix that is used for all elements within a schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "default_prefix",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "ifabsent": "default_ns",
                "rank": 11,
            }
        },
    )
    default_range: Optional[str] = Field(
        None,
        description="""default slot range to be used if range element is omitted from a slot definition""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "default_range",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "rank": 13,
            }
        },
    )
    types: Optional[Dict[str, TypeDefinition]] = Field(
        None,
        description="""An index to the collection of all type definitions in the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "types",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "rank": 6,
            }
        },
    )
    enums: Optional[Dict[str, EnumDefinition]] = Field(
        None,
        description="""An index to the collection of all enum definitions in the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "enums",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "rank": 5,
            }
        },
    )
    slots: Optional[Dict[str, SlotDefinition]] = Field(
        None,
        description="""An index to the collection of all slot definitions in the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "slots",
                "comments": [
                    "note the formal name of this element is slot_definitions, but "
                    "it has alias slots, which is the canonical form used in "
                    "yaml/json serializes of schemas."
                ],
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "rank": 4,
            }
        },
    )
    classes: Optional[Dict[str, ClassDefinition]] = Field(
        None,
        description="""An index to the collection of all class definitions in the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "classes",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "rank": 3,
            }
        },
    )
    metamodel_version: Optional[str] = Field(
        None,
        description="""Version of the metamodel used to load the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "metamodel_version",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "readonly": "supplied by the schema loader or schema view",
            }
        },
    )
    source_file: Optional[str] = Field(
        None,
        description="""name, uri or description of the source of the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "source_file",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "readonly": "supplied by the schema loader",
            }
        },
    )
    source_file_date: Optional[datetime] = Field(
        None,
        description="""modification date of the source of the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "source_file_date",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "readonly": "supplied by the loader",
            }
        },
    )
    source_file_size: Optional[int] = Field(
        None,
        description="""size in bytes of the source of the schema""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "source_file_size",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "readonly": "supplied by the schema loader or schema view",
            }
        },
    )
    generation_date: Optional[datetime] = Field(
        None,
        description="""date and time that the schema was loaded/generated""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "generation_date",
                "domain": "schema_definition",
                "domain_of": ["schema_definition"],
                "readonly": "supplied by the schema loader or schema view",
            }
        },
    )
    name: str = Field(
        ...,
        description="""a unique name for the schema that is both human-readable and consists of only characters from the NCName set""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "aliases": ["short name", "unique name"],
                "domain": "element",
                "domain_of": ["element"],
                "exact_mappings": ["schema:name"],
                "rank": 1,
                "see_also": ["https://en.wikipedia.org/wiki/Data_element_name"],
                "slot_uri": "rdfs:label",
            }
        },
    )
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "conforms_to",
                "domain": "element",
                "domain_of": ["element"],
                "slot_uri": "dcterms:conformsTo",
            }
        },
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )

    def model_post_init(self, __context):
        set_name(self.classes)
        set_name(self.types)
        set_name(self.enums)
        set_name(self.slots)


def set_name(d: dict | None) -> None:
    if not isinstance(d, dict):
        return None

    for k, v in d.items():
        v._name = k


class ClassDefinition(Definition):
    """
    an element whose instances are complex objects that may have slot-value assignments
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": ["table", "record", "template", "message", "observation"],
            "close_mappings": ["owl:Class"],
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "slot_usage": {
                "is_a": {
                    "description": "A primary parent class from which "
                    "inheritable metaslots are propagated",
                    "name": "is_a",
                    "range": "class_definition",
                },
                "mixins": {
                    "description": "A collection of secondary parent "
                    "mixin classes from which "
                    "inheritable metaslots are "
                    "propagated",
                    "name": "mixins",
                    "range": "class_definition",
                },
            },
        }
    )

    slots: Optional[List[str]] = Field(
        None,
        description="""collection of slot names that are applicable to a class""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "slots",
                "comments": [
                    "the list of applicable slots is inherited from parent classes",
                    "This defines the set of slots that are allowed to be used for a "
                    "given class. The final list of slots for a class is the "
                    "combination of the parent (is a) slots, mixins slots, apply to "
                    "slots minus the slot usage entries.",
                ],
                "domain": "class_definition",
                "domain_of": ["class_definition"],
                "rank": 19,
            }
        },
    )
    slot_usage: Optional[Dict[str, SlotDefinition]] = Field(
        None,
        description="""the refinement of a slot in the context of the containing class definition.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "slot_usage",
                "comments": [
                    "Many slots may be re-used across different classes, but the "
                    "meaning of the slot may be refined by context. For example, a "
                    "generic association model may use slots "
                    "subject/predicate/object with generic semantics and minimal "
                    "constraints. When this is subclasses, e.g. to disease-phenotype "
                    "associations then slot usage may specify both local naming "
                    "(e.g. subject=disease) and local constraints"
                ],
                "domain": "class_definition",
                "domain_of": ["class_definition"],
                "rank": 23,
            }
        },
    )
    attributes: Optional[Dict[str, SlotDefinition]] = Field(
        None,
        description="""Inline definition of slots""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "attributes",
                "comments": [
                    "attributes are an alternative way of defining new slots.  An "
                    "attribute adds a slot to the global space in the form "
                    "<class_name>__<slot_name> (lower case, double underscores).  "
                    "Attributes can be specialized via slot_usage."
                ],
                "domain": "class_definition",
                "domain_of": ["class_definition"],
                "rank": 29,
            }
        },
    )
    class_uri: Optional[str] = Field(
        None,
        description="""URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "class_uri",
                "aliases": ["public ID"],
                "comments": [
                    "Assigning class_uris can provide additional hooks for "
                    "interoperation, indicating a common conceptual model"
                ],
                "domain": "class_definition",
                "domain_of": ["class_definition"],
                "ifabsent": "class_curie",
                "rank": 2,
                "see_also": [
                    "linkml:definition_uri",
                    "https://linkml.io/linkml/schemas/uris-and-mappings.html",
                ],
            }
        },
    )
    tree_root: Optional[bool] = Field(
        None,
        description="""Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "tree_root",
                "domain": "class_definition",
                "domain_of": ["class_definition"],
                "notes": ["each schema should have at most one tree root"],
                "rank": 31,
                "see_also": ["https://linkml.io/linkml/intro/tutorial02.html"],
            }
        },
    )
    any_of: Optional[List[str]] = Field(
        None,
        description="""holds if at least one of the expressions hold""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "any_of",
                "domain_of": ["class_definition"],
                "exact_mappings": ["sh:or"],
                "is_a": "boolean_slot",
                "rank": 101,
                "see_also": [
                    "https://w3id.org/linkml/docs/specification/05validation/#rules"
                ],
            }
        },
    )
    exactly_one_of: Optional[List[str]] = Field(
        None,
        description="""holds if only one of the expressions hold""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "exactly_one_of",
                "domain_of": ["class_definition"],
                "exact_mappings": ["sh:xone"],
                "is_a": "boolean_slot",
                "rank": 103,
                "see_also": [
                    "https://w3id.org/linkml/docs/specification/05validation/#rules"
                ],
            }
        },
    )
    none_of: Optional[List[str]] = Field(
        None,
        description="""holds if none of the expressions hold""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "none_of",
                "domain_of": ["class_definition"],
                "exact_mappings": ["sh:not"],
                "is_a": "boolean_slot",
                "rank": 105,
                "see_also": [
                    "https://w3id.org/linkml/docs/specification/05validation/#rules"
                ],
            }
        },
    )
    all_of: Optional[List[str]] = Field(
        None,
        description="""holds if all of the expressions hold""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "all_of",
                "domain_of": ["class_definition"],
                "exact_mappings": ["sh:and"],
                "is_a": "boolean_slot",
                "rank": 107,
                "see_also": [
                    "https://w3id.org/linkml/docs/specification/05validation/#rules"
                ],
            }
        },
    )
    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class from which inheritable metaslots are propagated""",
        json_schema_extra={
            "linkml_meta": {
                "abstract": True,
                "alias": "is_a",
                "domain_of": ["definition"],
                "rank": 11,
            }
        },
    )
    abstract: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "abstract",
                "domain": "definition",
                "domain_of": ["definition"],
            }
        },
    )
    mixin: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "mixin",
                "aliases": ["trait"],
                "domain": "definition",
                "domain_of": ["definition"],
                "see_also": ["https://en.wikipedia.org/wiki/Mixin"],
            }
        },
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent mixin classes from which inheritable metaslots are propagated""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "mixins",
                "aliases": ["traits"],
                "comments": [
                    "mixins act in the same way as parents (is_a). They allow a "
                    "model to have a primary strict hierarchy, while keeping the "
                    "benefits of multiple inheritance"
                ],
                "domain_of": ["definition"],
                "rank": 13,
                "see_also": ["https://en.wikipedia.org/wiki/Mixin"],
            }
        },
    )
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "conforms_to",
                "domain": "element",
                "domain_of": ["element"],
                "slot_uri": "dcterms:conformsTo",
            }
        },
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )


class SlotDefinition(Definition):
    """
    an element that describes how instances are related to other instances
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": ["slot", "field", "property", "attribute", "column", "variable"],
            "close_mappings": ["rdf:Property", "qb:ComponentProperty"],
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "rank": 3,
        }
    )

    singular_name: Optional[str] = Field(
        None,
        description="""a name that is used in the singular form""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "singular_name",
                "close_mappings": ["skos:altLabel"],
                "comments": [
                    "this may be used in some schema translations where use of a "
                    "singular form is idiomatic, for example RDF"
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
            }
        },
    )
    slot_uri: Optional[str] = Field(
        None,
        description="""URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "slot_uri",
                "aliases": ["public ID"],
                "comments": [
                    "Assigning slot_uris can provide additional hooks for "
                    "interoperation, indicating a common conceptual model"
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "ifabsent": "slot_curie",
                "rank": 2,
                "see_also": [
                    "linkml:definition_uri",
                    "https://linkml.io/linkml/schemas/uris-and-mappings.html",
                ],
            }
        },
    )
    key: Optional[bool] = Field(
        None,
        description="""True means that the key slot(s) uniquely identify the elements within a single container""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "key",
                "comments": [
                    "key is inherited",
                    "a given domain can have at most one key slot (restriction to be "
                    "removed in the future)",
                    "identifiers and keys are mutually exclusive.  A given domain "
                    "cannot have both",
                    "a key slot is automatically required.  Keys cannot be optional",
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "see_also": ["linkml:unique_keys"],
            }
        },
    )
    identifier: Optional[bool] = Field(
        None,
        description="""True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "identifier",
                "aliases": ["primary key", "ID", "UID", "code"],
                "comments": [
                    "identifier is inherited",
                    "a key slot is automatically required.  Identifiers cannot be "
                    "optional",
                    "a given domain can have at most one identifier",
                    "identifiers and keys are mutually exclusive.  A given domain "
                    "cannot have both",
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "rank": 5,
                "see_also": [
                    "https://en.wikipedia.org/wiki/Identifier",
                    "linkml:unique_keys",
                ],
            }
        },
    )
    alias: Optional[str] = Field(
        None,
        description="""the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "alias",
                "comments": [
                    "an example of alias is used within this metamodel, "
                    "slot_definitions is aliases as slots",
                    "not to be confused with aliases, which indicates a set of terms "
                    "to be used for search purposes.",
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "rank": 6,
                "slot_uri": "skos:prefLabel",
            }
        },
    )
    inverse: Optional[str] = Field(
        None,
        description="""indicates that any instance of d s r implies that there is also an instance of r s' d""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "inverse",
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "slot_uri": "owl:inverseOf",
            }
        },
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
        json_schema_extra={
            "linkml_meta": {
                "alias": "range",
                "aliases": ["value domain"],
                "comments": [
                    "range is underspecified, as not all elements can appear as the "
                    "range of a slot."
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "ifabsent": "default_range",
                "inherited": True,
            }
        },
    )
    required: Optional[bool] = Field(
        None,
        description="""true means that the slot must be present in instances of the class definition""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "required",
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "rank": 8,
            }
        },
    )
    recommended: Optional[bool] = Field(
        None,
        description="""true means that the slot should be present in instances of the class definition, but this is not required""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "recommended",
                "comments": [
                    "This is to be used where not all data is expected to conform to "
                    "having a required field",
                    "If a slot is recommended, and it is not populated, applications "
                    "must not treat this as an error. Applications may use this to "
                    "inform the user of missing data",
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "rank": 9,
                "see_also": ["https://github.com/linkml/linkml/issues/177"],
            }
        },
    )
    multivalued: Optional[bool] = Field(
        None,
        description="""true means that slot can have more than one value and should be represented using a list or collection structure.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "multivalued",
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "rank": 7,
            }
        },
    )
    inlined: Optional[bool] = Field(
        None,
        description="""True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "inlined",
                "comments": [
                    "classes without keys or identifiers are necessarily inlined as "
                    "lists",
                    "only applicable in tree-like serializations, e.g json, yaml",
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "rank": 25,
                "see_also": [
                    "https://w3id.org/linkml/docs/specification/06mapping/#collection-forms",
                    "https://linkml.io/linkml/schemas/inlining.html",
                ],
            }
        },
    )
    inlined_as_list: Optional[bool] = Field(
        None,
        description="""True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "inlined_as_list",
                "comments": [
                    "The default loader will accept either list or dictionary form "
                    "as input.  This parameter controls internal\n"
                    "representation and output.",
                    "A keyed or identified class with one additional slot can be "
                    "input in a third form, a dictionary whose key\n"
                    "is the key or identifier and whose value is the one additional "
                    "element.  This form is still stored according\n"
                    "to the inlined_as_list setting.",
                ],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "rank": 27,
                "see_also": [
                    "https://w3id.org/linkml/docs/specification/06mapping/#collection-forms",
                    "https://linkml.io/linkml/schemas/inlining.html",
                ],
            }
        },
    )
    minimum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or higher than this""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "minimum_value",
                "aliases": ["low value"],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "notes": [
                    'Range to be refined to an "Ordinal" metaclass - see '
                    "https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142"
                ],
            }
        },
    )
    maximum_value: Optional[Any] = Field(
        None,
        description="""For ordinal ranges, the value must be equal to or lower than this""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "maximum_value",
                "aliases": ["high value"],
                "domain": "slot_definition",
                "domain_of": ["slot_definition"],
                "inherited": True,
                "notes": [
                    'Range to be refined to an "Ordinal" metaclass - see '
                    "https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142"
                ],
            }
        },
    )
    pattern: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "pattern",
                "domain": "definition",
                "domain_of": ["slot_definition", "type_definition"],
                "inherited": True,
                "rank": 35,
            }
        },
    )
    unit: Optional[str] = Field(
        None,
        description="""an encoding of a unit""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "unit",
                "domain_of": ["slot_definition"],
                "slot_uri": "qudt:unit",
            }
        },
    )
    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""",
        json_schema_extra={
            "linkml_meta": {
                "abstract": True,
                "alias": "is_a",
                "domain_of": ["definition"],
                "rank": 11,
            }
        },
    )
    abstract: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "abstract",
                "domain": "definition",
                "domain_of": ["definition"],
            }
        },
    )
    mixin: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "mixin",
                "aliases": ["trait"],
                "domain": "definition",
                "domain_of": ["definition"],
                "see_also": ["https://en.wikipedia.org/wiki/Mixin"],
            }
        },
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "mixins",
                "aliases": ["traits"],
                "comments": [
                    "mixins act in the same way as parents (is_a). They allow a "
                    "model to have a primary strict hierarchy, while keeping the "
                    "benefits of multiple inheritance"
                ],
                "domain_of": ["definition"],
                "rank": 13,
                "see_also": ["https://en.wikipedia.org/wiki/Mixin"],
            }
        },
    )
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "conforms_to",
                "domain": "element",
                "domain_of": ["element"],
                "slot_uri": "dcterms:conformsTo",
            }
        },
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )


class EnumDefinition(Definition):
    """
    an element whose instances must be drawn from a specified set of permissible values
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": [
                "enum",
                "enumeration",
                "semantic enumeration",
                "value set",
                "term set",
                "concept set",
                "code set",
                "Terminology Value Set",
                "answer list",
                "value domain",
            ],
            "close_mappings": ["skos:ConceptScheme"],
            "exact_mappings": [
                "qb:HierarchicalCodeList",
                "NCIT:C113497",
                "cdisc:ValueDomain",
            ],
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "rank": 5,
        }
    )

    enum_uri: Optional[str] = Field(
        None,
        description="""URI of the enum that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "enum_uri",
                "aliases": ["public ID"],
                "domain": "enum_definition",
                "domain_of": ["enum_definition"],
                "ifabsent": "class_curie",
            }
        },
    )
    permissible_values: Optional[Dict[str, PermissibleValue]] = Field(
        None,
        description="""A list of possible values for a slot range""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "permissible_values",
                "aliases": ["coded values"],
                "domain_of": ["enum_definition"],
                "exact_mappings": ["cdisc:PermissibleValue"],
            }
        },
    )
    is_a: Optional[str] = Field(
        None,
        description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""",
        json_schema_extra={
            "linkml_meta": {
                "abstract": True,
                "alias": "is_a",
                "domain_of": ["definition"],
                "rank": 11,
            }
        },
    )
    abstract: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "abstract",
                "domain": "definition",
                "domain_of": ["definition"],
            }
        },
    )
    mixin: Optional[bool] = Field(
        None,
        description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "mixin",
                "aliases": ["trait"],
                "domain": "definition",
                "domain_of": ["definition"],
                "see_also": ["https://en.wikipedia.org/wiki/Mixin"],
            }
        },
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "mixins",
                "aliases": ["traits"],
                "comments": [
                    "mixins act in the same way as parents (is_a). They allow a "
                    "model to have a primary strict hierarchy, while keeping the "
                    "benefits of multiple inheritance"
                ],
                "domain_of": ["definition"],
                "rank": 13,
                "see_also": ["https://en.wikipedia.org/wiki/Mixin"],
            }
        },
    )
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "conforms_to",
                "domain": "element",
                "domain_of": ["element"],
                "slot_uri": "dcterms:conformsTo",
            }
        },
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )


class TypeDefinition(Element):
    """
    an element that whose instances are atomic scalar values that can be mapped to primitive types
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "rank": 4,
        }
    )

    typeof: Optional[str] = Field(
        None,
        description="""A parent type from which type properties are inherited""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "typeof",
                "comments": [
                    "the target type definition of the typeof slot is referred to as "
                    'the "parent type"',
                    "the type definition containing the typeof slot is referred to "
                    'as the "child type"',
                    "type definitions without a typeof slot are referred to as a "
                    '"root type"',
                ],
                "domain": "type_definition",
                "domain_of": ["type_definition"],
                "rank": 7,
            }
        },
    )
    base: Optional[str] = Field(
        None,
        description="""python base type in the LinkML runtime that implements this type definition""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "base",
                "comments": [
                    "every root type must have a base",
                    "the base is inherited by child types but may be overridden.  "
                    "Base compatibility is not checked.",
                ],
                "domain": "type_definition",
                "domain_of": ["type_definition"],
                "inherited": True,
                "rank": 8,
            }
        },
    )
    uri: Optional[str] = Field(
        None,
        description="""The uri that defines the possible values for the type definition""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "uri",
                "comments": [
                    "uri is typically drawn from the set of URI's defined in OWL "
                    "(https://www.w3.org/TR/2012/REC-owl2-syntax-20121211/#Datatype_Maps)",
                    "every root type must have a type uri",
                ],
                "domain": "type_definition",
                "domain_of": ["type_definition"],
                "inherited": True,
                "rank": 2,
            }
        },
    )
    repr: Optional[str] = Field(
        None,
        description="""the name of the python object that implements this type definition""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "repr",
                "domain": "type_definition",
                "domain_of": ["type_definition"],
                "inherited": True,
                "rank": 10,
            }
        },
    )
    pattern: Optional[str] = Field(
        None,
        description="""the string value of the slot must conform to this regular expression expressed in the string""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "pattern",
                "domain": "definition",
                "domain_of": ["slot_definition", "type_definition"],
                "inherited": True,
                "rank": 35,
            }
        },
    )
    conforms_to: Optional[str] = Field(
        None,
        description="""An established standard to which the element conforms.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "conforms_to",
                "domain": "element",
                "domain_of": ["element"],
                "slot_uri": "dcterms:conformsTo",
            }
        },
    )
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )


class PermissibleValue(CommonMetadata):
    """
    a permissible value, accompanied by intended text and an optional mapping to a concept URI
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": ["PV"],
            "close_mappings": ["skos:Concept"],
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "mixins": ["common_metadata"],
            "rank": 16,
            "slot_usage": {
                "is_a": {"name": "is_a", "range": "permissible_value"},
                "mixins": {"name": "mixins", "range": "permissible_value"},
            },
        }
    )

    # text: str = Field(..., description="""The actual permissible value itself""", json_schema_extra = { "linkml_meta": {'alias': 'text',
    #     'aliases': ['value'],
    #     'close_mappings': ['skos:notation'],
    #     'comments': ['there are no constraints on the text of the permissible value, '
    #                  'but for many applications you may want to consider following '
    #                  'idiomatic forms and using computer-friendly forms'],
    #     'domain': 'permissible_value',
    #     'domain_of': ['permissible_value'],
    #     'rank': 21} })
    description: Optional[str] = Field(
        None,
        description="""a textual description of the element's purpose and use""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "aliases": ["definition"],
                "domain": "element",
                "domain_of": ["common_metadata", "permissible_value"],
                "exact_mappings": ["dcterms:description", "schema:description"],
                "rank": 5,
                "recommended": True,
                "slot_uri": "skos:definition",
            }
        },
    )
    meaning: Optional[str] = Field(
        None,
        description="""the value meaning of a permissible value""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "meaning",
                "aliases": ["PV meaning"],
                "domain": "permissible_value",
                "domain_of": ["permissible_value"],
                "notes": [
                    "we may want to change the range of this (and other) elements in "
                    "the model to an entitydescription type construct"
                ],
                "rank": 23,
                "see_also": ["https://en.wikipedia.org/wiki/ISO/IEC_11179"],
            }
        },
    )


class Prefix(ConfiguredBaseModel):
    """
    prefix URI tuple
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://data.netbeheernederland.nl/meta/linkml-prof-logical-model",
            "rank": 12,
        }
    )

    prefix_prefix: str = Field(
        ...,
        description="""The prefix components of a prefix expansions. This is the part that appears before the colon in a CURIE.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefix_prefix",
                "domain": "prefix",
                "domain_of": ["prefix"],
                "rank": 1,
                "slot_uri": "sh:prefix",
            }
        },
    )
    prefix_reference: str = Field(
        ...,
        description="""The namespace to which a prefix expands to.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "prefix_reference",
                "domain": "prefix",
                "domain_of": ["prefix"],
                "rank": 2,
                "slot_uri": "sh:namespace",
            }
        },
    )


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Expression.model_rebuild()
Element.model_rebuild()
Definition.model_rebuild()
ClassDefinition.model_rebuild()
SlotDefinition.model_rebuild()
