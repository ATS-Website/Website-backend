from rest_framework.serializers import ModelSerializer
from Blogs.models import *

class AuthorSerializer(ModelSerializer):
   class Meta:
      model= Author
      fields= ['id',
         'first_name', 'last_name', 'email',
         'author_bio', 'author_profile_pics',
      ]

class BlogArticleSerializer(ModelSerializer):
   class Meta:
      model= BlogArticle
      fields= ['id', 'article_title', 'article_intro', 'article_description',
      'created_at', 'updated_at', 'tags', 'author', 'image',
      'is_active',]


class CommentSerializer(ModelSerializer):
   class Meta:
      model= Comment
      fields= ['id', 'commenter_name', 'your_comment', 'created_at' ]


# NEWS SERIALIZER
class NewsArticleSerializer(ModelSerializer):
   class Meta:
      model=NewsArticle
      fields=  ['id', 'news_title', 'news_intro', 'news_description',
      'category', 'author', 'image',
      'is_active',]
      

class NewsCommentSerializer(ModelSerializer):
   class Meta:
      model= NewsComment
      fields= ['id', 'commenter_name', 'your_comment', 'created_at' ]

#GALLERY
class GallerySerializer(ModelSerializer):
   class Meta:
      model= Gallery
      fields= ['id', 'images', 'text']

# NEWSLETTER
class NewsLetterSubscriptionSerializer(ModelSerializer):
   class Meta:
      model = NewsLetterSubscription
      fields= ['id', 'email']
