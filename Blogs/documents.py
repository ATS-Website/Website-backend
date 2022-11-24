# articles/documents.py

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import NewsArticle, BlogArticle


@registry.register_document
class NewsArticleDocument(Document):
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

    class Index:
        name = 'blogs'

    class Django:
        model = BlogArticle
        # fields = [
        #     "title",
        #     "description",
        #     "category",
        #     "created_at",
        #     "updated_at",
        # ]
