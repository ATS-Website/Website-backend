from django.shortcuts import render
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from Blogs.model import Blog

# Create your views here.


def is_blog_published(self):
    return self.is_published


@register(Blog)
class BlogsIndex(AlgoliaIndex):
    model = Blog
    shoud_index = 'is_blog_published'
    fields = [
        'title',
        'content',
    ]

    settings = {
        "searchableAttributes": ["title", "content"],
        "attributesForFaceting": []
    }


@register(Blog)
class NewsIndex(AlgoliaIndex):
    model = New
    fields = [
        'title',
        'content',
        'get_absolute_url'
    ]
    settings = {
        "searchableAttributes": ["title", "content"],
        "attributesForFaceting": []
    }
