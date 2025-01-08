from linkml_asciidoc_generator.linkml.model import LinkMLClass, LinkMLSchema
from linkml_asciidoc_generator.config import Config
from linkml_asciidoc_generator.asciidoc.class_page.model import (
    ClassPage,
    Class,
    RelationsDiagram,
    AttributesDiagram,
)
from linkml_asciidoc_generator.linkml.query import (
    get_ancestors,
    get_relations,
    get_attributes,
)


def _generate_class(class_: LinkMLClass, schema: LinkMLSchema, config: Config) -> Class:
    _class_ = Class(
        name=class_._meta["name"],
        is_abstract=bool(class_.abstract),
        is_mixin=bool(class_.mixin),
        uri=class_.class_uri,
        ancestors=[c._meta["name"] for c in get_ancestors(class_, schema)],
        # relations=list(get_relations(class_, schema).values()),
        # attributes=list(get_attributes(class_, schema).values()),
        relations=get_relations(class_, schema),
        attributes=get_attributes(class_, schema),
    )

    return _class_


def generate_class_page(
    class_: LinkMLClass, schema: LinkMLSchema, config: Config
) -> ClassPage:
    _class_ = _generate_class(class_, schema, config)

    attributes_diagram = None

    if config["diagrams"]["relations"]:
        relations_diagram = RelationsDiagram(
            name=f"{_class_.name}_relations",
            template=config["templates"]["class_page_relations_diagram"],
            class_=_class_,
        )
    else:
        relations_diagram = None

    page = ClassPage(
        name=_class_.name,
        template=config["templates"]["class_page"],
        title=class_.title or _class_.name,
        class_=_class_,
        relations_diagram=relations_diagram,
        attributes_diagram=attributes_diagram,
    )

    return page


# class RelationsDiagram(MermaidDiagram):
#     class_name: LinkMLClassName

#     return page
#     # relations_diagram: RelationsDiagram | None = None
