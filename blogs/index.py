from django.shortcuts import render
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from blogs.models import BlogArticle, NewsArticle


# Create your views here.


# def is_blog_published(self):
#     return self.is_published


@register(BlogArticle)
class BlogsIndex(AlgoliaIndex):
    model = BlogArticle
    fields = [
        'title',
        'intro',
        'description',
        'author'
    ]

    settings = {
        "searchableAttributes": ['title',
                                 'intro',
                                 'description', 'author', ],
        "attributesForFaceting": []
    }


@register(NewsArticle)
class NewsIndex(AlgoliaIndex):
    model = NewsArticle
    fields = [
        'title',
        'intro',
        'description',
        'author',
        'category',

    ]
    settings = {
        "searchableAttributes": ["title", "content", 'author', ],
        "attributesForFaceting": []
    }
