# articles/documents.py

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
# from oscar.core.loading import get_model

from .models import NewsArticle, BlogArticle

# Product = get_model('catalogue', 'product')


@registry.register_document
class NewsArticleDocument(Document):
    id = fields.IntegerField()
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    description = fields.TextField(
        attr='description',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    intro = fields.TextField(
        attr='intro',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    image = fields.FileField()
    category = fields.ObjectField(
        attr='category',
        properties={
            'id': fields.IntegerField(),
            'name': fields.TextField(
                attr='name',
                fields={
                    'raw': fields.KeywordField(),
                }
            )
        }
    )
    author = fields.ObjectField(
        attr='author',
        properties={
            'id': fields.IntegerField(),
            'first_name': fields.TextField(
                attr='first_name',
                fields={
                    'raw': fields.KeywordField(),
                }
            ),
            'last_name': fields.TextField(
                attr='last_name',
                fields={
                    'raw': fields.KeywordField(),
                }
            )
        }
    )
    created_at = fields.DateField()

    class Index:
        name = 'news'

    class Django:
        model = NewsArticle
        # fields = [
        #     "title",
        #     "description",
        #     "category",
        #     "created_at",
        #     "updated_at",
        # ]


@registry.register_document
class BlogArticleDocument(Document):
    id = fields.IntegerField()
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    description = fields.TextField(
        attr='description',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    intro = fields.TextField(
        attr='intro',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )
    image = fields.FileField()
    author = fields.ObjectField(
        attr='author',
        properties={
            'id': fields.IntegerField(),
            'first_name': fields.TextField(
                attr='name',
                fields={
                    'raw': fields.KeywordField(),
                }
            ),
            'last_name': fields.TextField(
                attr='last_name',
                fields={
                    'raw': fields.KeywordField(),
                }
            )
        }
    )
    created_at = fields.DateField()

    class Index:
        name = 'blogs'

    class Django:
        model = BlogArticle
        fields = [

            # "title",
            # "description",
            # "category",
            # "created_at",
            # "updated_at",
        ]
