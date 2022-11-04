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
                  'created_at', 'updated_at', 'tags', 'author', 'url', 'image',
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
        fields = ['id', 'title', 'intro', 'description',
                  'category', 'author', 'image', 'url',
                  ]

    def get_url(self, obj):
        return self.context.get("request").build_absolute_uri("/api/v1/news/") + str(obj.pk)


class NewsCommentSerializer(ModelSerializer):
    news_article = NewsArticleSerializer(read_only=True)

    class Meta:
        model = NewsComment
        fields = ['id', 'name', 'description', 'news_article', 'created_at']

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
