from linkml_asciidoc_generator.linkml.model import LinkMLClass, LinkMLSchema
from linkml_asciidoc_generator.asciidoc.model import Config
from linkml_asciidoc_generator.asciidoc.model.class_page import ClassPage, Class, RelationsDiagram, AttributesDiagram
from linkml_asciidoc_generator.asciidoc.generate.helper.template import read_jinja2_template
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
        relations=list(get_relations(class_, schema).values()),
        attributes=list(get_attributes(class_, schema).values()),
    )

    return _class_


def generate_class_page(
    class_: LinkMLClass, schema: LinkMLSchema, config: Config
) -> ClassPage:
    _class_ = _generate_class(class_, schema, config)

    if config.get("include_relations_diagram"):
        relations_diagram = RelationsDiagram(name=f"{_class_.name}_relations", template=read_jinja2_template(config.))



    page = ClassPage(
        name=_class_.name, title=class_.title or _class_.name, class_=_class_,
class MermaidDiagram(Resource):
    template: Jinja2Template


class RelationsDiagram(MermaidDiagram):
    class_name: LinkMLClassName

    return page
    # relations_diagram: RelationsDiagram | None = None
    # attributes_diagram: AttributesDiagram | None = None
