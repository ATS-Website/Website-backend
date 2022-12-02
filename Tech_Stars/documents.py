# articles/documents.py

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import TechStar


@registry.register_document
class TechStarDocument(Document):
    id = fields.IntegerField()
    tech_star_id = fields.TextField()
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
    date_created = fields.DateField()
    profile_picture = fields.FileField()
    course = fields.TextField(
        attr='course',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    official_email = fields.TextField()

    favorite_meal = fields.TextField(
        attr='favourite_meal',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    favorite_quote = fields.TextField(
        attr='favourite_quote',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    cohort = fields.TextField(
        attr='cohort',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    date_created = fields.DateField()

    class Index:
        name = 'techstars'

    class Django:
        model = TechStar
