# articles/documents.py

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import TechStar


@registry.register_document
class TechStarDocument(Document):
    full_name = fields.TextField(
        attr='full_name',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    self_description = fields.TextField(
        attr='self_description',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )

    class Index:
        name = 'techstars'

    class Django:
        model = TechStar
