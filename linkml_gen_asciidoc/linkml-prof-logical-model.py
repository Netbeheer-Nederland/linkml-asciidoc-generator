from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "ignore",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_curi_maps': ['semweb_context'],
     'default_prefix': 'linkml',
     'default_range': 'string',
     'description': 'A profile of the LinkML Schema metamodel to represent logical '
                    'models in. The emphasis is on structural description and '
                    'semantic alignment. Another aim is the avoidance of '
                    'complicated and vague language semantics to improve ease of '
                    'use and consistency in how schemas are interpreted, most '
                    'notably by generators.',
     'emit_prefixes': ['linkml',
                       'rdf',
                       'rdfs',
                       'xsd',
                       'skos',
                       'dcterms',
                       'OIO',
                       'owl',
                       'pav'],
     'id': 'http://data.netbeheernederland.nl/meta/linkml-prof-logical-model',
     'imports': ['linkml:types'],
     'license': 'https://www.apache.org/licenses/LICENSE-2.0',
     'name': 'linkml-prof-logical-model',
     'prefixes': {'IAO': {'prefix_prefix': 'IAO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/IAO_'},
                  'NCIT': {'prefix_prefix': 'NCIT',
                           'prefix_reference': 'http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'},
                  'OIO': {'prefix_prefix': 'OIO',
                          'prefix_reference': 'http://www.geneontology.org/formats/oboInOwl#'},
                  'SIO': {'prefix_prefix': 'SIO',
                          'prefix_reference': 'http://semanticscience.org/resource/SIO_'},
                  'bibo': {'prefix_prefix': 'bibo',
                           'prefix_reference': 'http://purl.org/ontology/bibo/'},
                  'cdisc': {'prefix_prefix': 'cdisc',
                            'prefix_reference': 'http://rdf.cdisc.org/mms#'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'oslc': {'prefix_prefix': 'oslc',
                           'prefix_reference': 'http://open-services.net/ns/core#'},
                  'owl': {'prefix_prefix': 'owl',
                          'prefix_reference': 'http://www.w3.org/2002/07/owl#'},
                  'pav': {'prefix_prefix': 'pav',
                          'prefix_reference': 'http://purl.org/pav/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'qb': {'prefix_prefix': 'qb',
                         'prefix_reference': 'http://purl.org/linked-data/cube#'},
                  'qudt': {'prefix_prefix': 'qudt',
                           'prefix_reference': 'http://qudt.org/schema/qudt/'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'sh': {'prefix_prefix': 'sh',
                         'prefix_reference': 'http://www.w3.org/ns/shacl#'},
                  'shex': {'prefix_prefix': 'shex',
                           'prefix_reference': 'http://www.w3.org/ns/shex#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'skosxl': {'prefix_prefix': 'skosxl',
                             'prefix_reference': 'http://www.w3.org/2008/05/skos-xl#'},
                  'swrl': {'prefix_prefix': 'swrl',
                           'prefix_reference': 'http://www.w3.org/2003/11/swrl#'},
                  'vann': {'prefix_prefix': 'vann',
                           'prefix_reference': 'https://vocab.org/vann/'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'source_file': 'spec/meta.yaml',
     'title': 'LinkML Schema Metamodel: `LogicalModel` Profile'} )


class Expression(ConfiguredBaseModel):
    """
    general mixin for any class that can represent some form of expression
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'http://data.netbeheernederland.nl/meta/linkml-prof-logical-model',
         'mixin': True})

    pass


class Element(ConfiguredBaseModel):
    """
    A named element in the model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'aliases': ['data element', 'object'],
         'from_schema': 'http://data.netbeheernederland.nl/meta/linkml-prof-logical-model',
         'see_also': ['https://en.wikipedia.org/wiki/Data_element']})

    name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name'],
         'slot_uri': 'rdfs:label'} })
    conforms_to: Optional[str] = Field(None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'alias': 'conforms_to',
         'domain': 'element',
         'domain_of': ['element'],
         'slot_uri': 'dcterms:conformsTo'} })


class Definition(Element):
    """
    abstract base class for core metaclasses
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'http://data.netbeheernederland.nl/meta/linkml-prof-logical-model',
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_definition']})

    is_a: Optional[str] = Field(None, description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""", json_schema_extra = { "linkml_meta": {'abstract': True, 'alias': 'is_a', 'domain_of': ['definition'], 'rank': 11} })
    abstract: Optional[bool] = Field(None, description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""", json_schema_extra = { "linkml_meta": {'alias': 'abstract', 'domain': 'definition', 'domain_of': ['definition']} })
    mixin: Optional[bool] = Field(None, description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""", json_schema_extra = { "linkml_meta": {'alias': 'mixin',
         'aliases': ['trait'],
         'domain': 'definition',
         'domain_of': ['definition'],
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    mixins: Optional[List[str]] = Field(None, description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""", json_schema_extra = { "linkml_meta": {'alias': 'mixins',
         'aliases': ['traits'],
         'comments': ['mixins act in the same way as parents (is_a). They allow a '
                      'model to have a primary strict hierarchy, while keeping the '
                      'benefits of multiple inheritance'],
         'domain_of': ['definition'],
         'rank': 13,
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name'],
         'slot_uri': 'rdfs:label'} })
    conforms_to: Optional[str] = Field(None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'alias': 'conforms_to',
         'domain': 'element',
         'domain_of': ['element'],
         'slot_uri': 'dcterms:conformsTo'} })


class ClassDefinition(Definition):
    """
    an element whose instances are complex objects that may have slot-value assignments
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['table', 'record', 'template', 'message', 'observation'],
         'close_mappings': ['owl:Class'],
         'from_schema': 'http://data.netbeheernederland.nl/meta/linkml-prof-logical-model',
         'slot_usage': {'is_a': {'description': 'A primary parent class from which '
                                                'inheritable metaslots are propagated',
                                 'name': 'is_a',
                                 'range': 'class_definition'},
                        'mixins': {'description': 'A collection of secondary parent '
                                                  'mixin classes from which '
                                                  'inheritable metaslots are '
                                                  'propagated',
                                   'name': 'mixins',
                                   'range': 'class_definition'}}})

    slots: Optional[List[str]] = Field(None, description="""collection of slot names that are applicable to a class""", json_schema_extra = { "linkml_meta": {'alias': 'slots',
         'comments': ['the list of applicable slots is inherited from parent classes',
                      'This defines the set of slots that are allowed to be used for a '
                      'given class. The final list of slots for a class is the '
                      'combination of the parent (is a) slots, mixins slots, apply to '
                      'slots minus the slot usage entries.'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'rank': 19} })
    slot_usage: Optional[Dict[str, SlotDefinition]] = Field(None, description="""the refinement of a slot in the context of the containing class definition.""", json_schema_extra = { "linkml_meta": {'alias': 'slot_usage',
         'comments': ['Many slots may be re-used across different classes, but the '
                      'meaning of the slot may be refined by context. For example, a '
                      'generic association model may use slots '
                      'subject/predicate/object with generic semantics and minimal '
                      'constraints. When this is subclasses, e.g. to disease-phenotype '
                      'associations then slot usage may specify both local naming '
                      '(e.g. subject=disease) and local constraints'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'rank': 23} })
    attributes: Optional[Dict[str, SlotDefinition]] = Field(None, description="""Inline definition of slots""", json_schema_extra = { "linkml_meta": {'alias': 'attributes',
         'comments': ['attributes are an alternative way of defining new slots.  An '
                      'attribute adds a slot to the global space in the form '
                      '<class_name>__<slot_name> (lower case, double underscores).  '
                      'Attributes can be specialized via slot_usage.'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'rank': 29} })
    class_uri: Optional[str] = Field(None, description="""URI of the class that provides a semantic interpretation of the element in a linked data context. The URI may come from any namespace and may be shared between schemas""", json_schema_extra = { "linkml_meta": {'alias': 'class_uri',
         'aliases': ['public ID'],
         'comments': ['Assigning class_uris can provide additional hooks for '
                      'interoperation, indicating a common conceptual model'],
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'ifabsent': 'class_curie',
         'rank': 2,
         'see_also': ['linkml:definition_uri',
                      'https://linkml.io/linkml/schemas/uris-and-mappings.html']} })
    tree_root: Optional[bool] = Field(None, description="""Indicates that this is the Container class which forms the root of the serialized document structure in tree serializations""", json_schema_extra = { "linkml_meta": {'alias': 'tree_root',
         'domain': 'class_definition',
         'domain_of': ['class_definition'],
         'notes': ['each schema should have at most one tree root'],
         'rank': 31,
         'see_also': ['https://linkml.io/linkml/intro/tutorial02.html']} })
    any_of: Optional[List[str]] = Field(None, description="""holds if at least one of the expressions hold""", json_schema_extra = { "linkml_meta": {'alias': 'any_of',
         'domain_of': ['class_definition'],
         'exact_mappings': ['sh:or'],
         'is_a': 'boolean_slot',
         'rank': 101,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    exactly_one_of: Optional[List[str]] = Field(None, description="""holds if only one of the expressions hold""", json_schema_extra = { "linkml_meta": {'alias': 'exactly_one_of',
         'domain_of': ['class_definition'],
         'exact_mappings': ['sh:xone'],
         'is_a': 'boolean_slot',
         'rank': 103,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    none_of: Optional[List[str]] = Field(None, description="""holds if none of the expressions hold""", json_schema_extra = { "linkml_meta": {'alias': 'none_of',
         'domain_of': ['class_definition'],
         'exact_mappings': ['sh:not'],
         'is_a': 'boolean_slot',
         'rank': 105,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    all_of: Optional[List[str]] = Field(None, description="""holds if all of the expressions hold""", json_schema_extra = { "linkml_meta": {'alias': 'all_of',
         'domain_of': ['class_definition'],
         'exact_mappings': ['sh:and'],
         'is_a': 'boolean_slot',
         'rank': 107,
         'see_also': ['https://w3id.org/linkml/docs/specification/05validation/#rules']} })
    is_a: Optional[str] = Field(None, description="""A primary parent class from which inheritable metaslots are propagated""", json_schema_extra = { "linkml_meta": {'abstract': True, 'alias': 'is_a', 'domain_of': ['definition'], 'rank': 11} })
    abstract: Optional[bool] = Field(None, description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""", json_schema_extra = { "linkml_meta": {'alias': 'abstract', 'domain': 'definition', 'domain_of': ['definition']} })
    mixin: Optional[bool] = Field(None, description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""", json_schema_extra = { "linkml_meta": {'alias': 'mixin',
         'aliases': ['trait'],
         'domain': 'definition',
         'domain_of': ['definition'],
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    mixins: Optional[List[str]] = Field(None, description="""A collection of secondary parent mixin classes from which inheritable metaslots are propagated""", json_schema_extra = { "linkml_meta": {'alias': 'mixins',
         'aliases': ['traits'],
         'comments': ['mixins act in the same way as parents (is_a). They allow a '
                      'model to have a primary strict hierarchy, while keeping the '
                      'benefits of multiple inheritance'],
         'domain_of': ['definition'],
         'rank': 13,
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name'],
         'slot_uri': 'rdfs:label'} })
    conforms_to: Optional[str] = Field(None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'alias': 'conforms_to',
         'domain': 'element',
         'domain_of': ['element'],
         'slot_uri': 'dcterms:conformsTo'} })


class SlotDefinition(Definition):
    """
    an element that describes how instances are related to other instances
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['slot', 'field', 'property', 'attribute', 'column', 'variable'],
         'close_mappings': ['rdf:Property', 'qb:ComponentProperty'],
         'from_schema': 'http://data.netbeheernederland.nl/meta/linkml-prof-logical-model',
         'rank': 3})

    singular_name: Optional[str] = Field(None, description="""a name that is used in the singular form""", json_schema_extra = { "linkml_meta": {'alias': 'singular_name',
         'close_mappings': ['skos:altLabel'],
         'comments': ['this may be used in some schema translations where use of a '
                      'singular form is idiomatic, for example RDF'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition']} })
    slot_uri: Optional[str] = Field(None, description="""URI of the class that provides a semantic interpretation of the slot in a linked data context. The URI may come from any namespace and may be shared between schemas.""", json_schema_extra = { "linkml_meta": {'alias': 'slot_uri',
         'aliases': ['public ID'],
         'comments': ['Assigning slot_uris can provide additional hooks for '
                      'interoperation, indicating a common conceptual model'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'ifabsent': 'slot_curie',
         'rank': 2,
         'see_also': ['linkml:definition_uri',
                      'https://linkml.io/linkml/schemas/uris-and-mappings.html']} })
    key: Optional[bool] = Field(None, description="""True means that the key slot(s) uniquely identify the elements within a single container""", json_schema_extra = { "linkml_meta": {'alias': 'key',
         'comments': ['key is inherited',
                      'a given domain can have at most one key slot (restriction to be '
                      'removed in the future)',
                      'identifiers and keys are mutually exclusive.  A given domain '
                      'cannot have both',
                      'a key slot is automatically required.  Keys cannot be optional'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'see_also': ['linkml:unique_keys']} })
    identifier: Optional[bool] = Field(None, description="""True means that the key slot(s) uniquely identifies the elements. There can be at most one identifier or key per container""", json_schema_extra = { "linkml_meta": {'alias': 'identifier',
         'aliases': ['primary key', 'ID', 'UID', 'code'],
         'comments': ['identifier is inherited',
                      'a key slot is automatically required.  Identifiers cannot be '
                      'optional',
                      'a given domain can have at most one identifier',
                      'identifiers and keys are mutually exclusive.  A given domain '
                      'cannot have both'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'rank': 5,
         'see_also': ['https://en.wikipedia.org/wiki/Identifier', 'linkml:unique_keys']} })
    alias: Optional[str] = Field(None, description="""the name used for a slot in the context of its owning class.  If present, this is used instead of the actual slot name.""", json_schema_extra = { "linkml_meta": {'alias': 'alias',
         'comments': ['an example of alias is used within this metamodel, '
                      'slot_definitions is aliases as slots',
                      'not to be confused with aliases, which indicates a set of terms '
                      'to be used for search purposes.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'rank': 6,
         'slot_uri': 'skos:prefLabel'} })
    inverse: Optional[str] = Field(None, description="""indicates that any instance of d s r implies that there is also an instance of r s' d""", json_schema_extra = { "linkml_meta": {'alias': 'inverse',
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'slot_uri': 'owl:inverseOf'} })
    range: Optional[str] = Field(None, description="""defines the type of the object of the slot.  Given the following slot definition
  S1:
    domain: C1
    range:  C2
the declaration
  X:
    S1: Y

implicitly asserts Y is an instance of C2
""", json_schema_extra = { "linkml_meta": {'alias': 'range',
         'aliases': ['value domain'],
         'comments': ['range is underspecified, as not all elements can appear as the '
                      'range of a slot.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'ifabsent': 'default_range',
         'inherited': True} })
    required: Optional[bool] = Field(None, description="""true means that the slot must be present in instances of the class definition""", json_schema_extra = { "linkml_meta": {'alias': 'required',
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'rank': 8} })
    recommended: Optional[bool] = Field(None, description="""true means that the slot should be present in instances of the class definition, but this is not required""", json_schema_extra = { "linkml_meta": {'alias': 'recommended',
         'comments': ['This is to be used where not all data is expected to conform to '
                      'having a required field',
                      'If a slot is recommended, and it is not populated, applications '
                      'must not treat this as an error. Applications may use this to '
                      'inform the user of missing data'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'rank': 9,
         'see_also': ['https://github.com/linkml/linkml/issues/177']} })
    multivalued: Optional[bool] = Field(None, description="""true means that slot can have more than one value and should be represented using a list or collection structure.""", json_schema_extra = { "linkml_meta": {'alias': 'multivalued',
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'rank': 7} })
    inlined: Optional[bool] = Field(None, description="""True means that keyed or identified slot appears in an outer structure by value.  False means that only the key or identifier for the slot appears within the domain, referencing a structure that appears elsewhere.""", json_schema_extra = { "linkml_meta": {'alias': 'inlined',
         'comments': ['classes without keys or identifiers are necessarily inlined as '
                      'lists',
                      'only applicable in tree-like serializations, e.g json, yaml'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'rank': 25,
         'see_also': ['https://w3id.org/linkml/docs/specification/06mapping/#collection-forms',
                      'https://linkml.io/linkml/schemas/inlining.html']} })
    inlined_as_list: Optional[bool] = Field(None, description="""True means that an inlined slot is represented as a list of range instances.  False means that an inlined slot is represented as a dictionary, whose key is the slot key or identifier and whose value is the range instance.""", json_schema_extra = { "linkml_meta": {'alias': 'inlined_as_list',
         'comments': ['The default loader will accept either list or dictionary form '
                      'as input.  This parameter controls internal\n'
                      'representation and output.',
                      'A keyed or identified class with one additional slot can be '
                      'input in a third form, a dictionary whose key\n'
                      'is the key or identifier and whose value is the one additional '
                      'element.  This form is still stored according\n'
                      'to the inlined_as_list setting.'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'rank': 27,
         'see_also': ['https://w3id.org/linkml/docs/specification/06mapping/#collection-forms',
                      'https://linkml.io/linkml/schemas/inlining.html']} })
    minimum_value: Optional[Any] = Field(None, description="""For ordinal ranges, the value must be equal to or higher than this""", json_schema_extra = { "linkml_meta": {'alias': 'minimum_value',
         'aliases': ['low value'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    maximum_value: Optional[Any] = Field(None, description="""For ordinal ranges, the value must be equal to or lower than this""", json_schema_extra = { "linkml_meta": {'alias': 'maximum_value',
         'aliases': ['high value'],
         'domain': 'slot_definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'notes': ['Range to be refined to an "Ordinal" metaclass - see '
                   'https://github.com/linkml/linkml/issues/1384#issuecomment-1892721142']} })
    pattern: Optional[str] = Field(None, description="""the string value of the slot must conform to this regular expression expressed in the string""", json_schema_extra = { "linkml_meta": {'alias': 'pattern',
         'domain': 'definition',
         'domain_of': ['slot_definition'],
         'inherited': True,
         'rank': 35} })
    unit: Optional[str] = Field(None, description="""an encoding of a unit""", json_schema_extra = { "linkml_meta": {'alias': 'unit', 'domain_of': ['slot_definition'], 'slot_uri': 'qudt:unit'} })
    is_a: Optional[str] = Field(None, description="""A primary parent class or slot from which inheritable metaslots are propagated from. While multiple inheritance is not allowed, mixins can be provided effectively providing the same thing. The semantics are the same when translated to formalisms that allow MI (e.g. RDFS/OWL). When translating to a SI framework (e.g. java classes, python classes) then is a is used. When translating a framework without polymorphism (e.g. json-schema, solr document schema) then is a and mixins are recursively unfolded""", json_schema_extra = { "linkml_meta": {'abstract': True, 'alias': 'is_a', 'domain_of': ['definition'], 'rank': 11} })
    abstract: Optional[bool] = Field(None, description="""Indicates the class or slot cannot be directly instantiated and is intended for grouping purposes.""", json_schema_extra = { "linkml_meta": {'alias': 'abstract', 'domain': 'definition', 'domain_of': ['definition']} })
    mixin: Optional[bool] = Field(None, description="""Indicates the class or slot is intended to be inherited from without being an is_a parent. mixins should not be inherited from using is_a, except by other mixins.""", json_schema_extra = { "linkml_meta": {'alias': 'mixin',
         'aliases': ['trait'],
         'domain': 'definition',
         'domain_of': ['definition'],
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    mixins: Optional[List[str]] = Field(None, description="""A collection of secondary parent classes or slots from which inheritable metaslots are propagated from.""", json_schema_extra = { "linkml_meta": {'alias': 'mixins',
         'aliases': ['traits'],
         'comments': ['mixins act in the same way as parents (is_a). They allow a '
                      'model to have a primary strict hierarchy, while keeping the '
                      'benefits of multiple inheritance'],
         'domain_of': ['definition'],
         'rank': 13,
         'see_also': ['https://en.wikipedia.org/wiki/Mixin']} })
    name: str = Field(..., description="""the unique name of the element within the context of the schema.  Name is combined with the default prefix to form the globally unique subject of the target class.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'aliases': ['short name', 'unique name'],
         'domain': 'element',
         'domain_of': ['element'],
         'exact_mappings': ['schema:name'],
         'rank': 1,
         'see_also': ['https://en.wikipedia.org/wiki/Data_element_name'],
         'slot_uri': 'rdfs:label'} })
    conforms_to: Optional[str] = Field(None, description="""An established standard to which the element conforms.""", json_schema_extra = { "linkml_meta": {'alias': 'conforms_to',
         'domain': 'element',
         'domain_of': ['element'],
         'slot_uri': 'dcterms:conformsTo'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Expression.model_rebuild()
Element.model_rebuild()
Definition.model_rebuild()
ClassDefinition.model_rebuild()
SlotDefinition.model_rebuild()

