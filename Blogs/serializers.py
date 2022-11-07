from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id',
                  'first_name', 'last_name', 'email',
                  'bio', 'profile_pics',
                  ]


class BlogArticleSerializer(ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = BlogArticle
        fields = ['id', 'title', 'intro', 'description',
                  'created_at', 'tags', 'author', 'url', 'image',
                  ]

    def get_url(self, obj):
        return self.context.get("request").build_absolute_uri("/api/v1/blogs/") + str(obj.pk)


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'description', 'created_at']


# NEWS SERIALIZER
class NewsArticleSerializer(ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'intro', 'description', 'created_at',
                  'category', 'author', 'image', 'url',
                  ]

    def get_url(self, obj):
        return self.context.get("request").build_absolute_uri("/api/v1/news/") + str(obj.pk)


class NewsCommentSerializer(ModelSerializer):
    class Meta:
        model = NewsComment
        fields = ['id', 'name', 'description', 'created_at']

# GALLERY


class GallerySerializer(ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'image', 'text']

# NEWSLETTER


class NewsLetterSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = NewsLetterSubscription
        fields = ['id', 'email']


class CategorySerializer(ModelSerializer):
    class Meta:
        model= Category
        fields= ['id', 'name']

class TagSerializer(ModelSerializer):
    class Meta:
        model= Tag
        fields= ['id', 'name']
