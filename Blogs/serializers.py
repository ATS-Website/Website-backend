from rest_framework.serializers import ModelSerializer
<<<<<<< HEAD
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from Blogs.models import *

class AuthorSerializer(ModelSerializer):
   
   class Meta:
      model= Author
      fields= ['id',
         'first_name', 'last_name', 'email',
         'author_bio', 'author_profile_pics',
         
      ]

class BlogSerializer(ModelSerializer):
   class Meta:
      model= Blog
      fields= ['id', 'blog_title', 'blog_intro', 'blog_description',
      'created_at', 'updated_at', 'tags', 'author', 'image',
      'is_active',]


class BlogCommentSerializer(ModelSerializer):
   class Meta:
      model= BlogComment
      fields= ['id', 'commenter_name', 'your_comment', 'created_at' ]


# NEWS SERIALIZER
class NewsSerializer(ModelSerializer):
   class Meta:
      model=News
      fields=  ['id', 'news_title', 'news_intro', 'news_description',
      'category', 'author', 'image',
      'is_active',]
      
=======
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

>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3

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
