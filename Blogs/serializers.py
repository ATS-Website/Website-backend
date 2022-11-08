from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework import serializers
from .models import *


class AuthorSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Blogs:author_detail_update", read_only=True)

    class Meta:
        model = Author
        fields = ['id',
                  'first_name', 'last_name', 'email',
                  'bio', 'profile_pics', "url"
                  ]


class AuthorDetailSerializer(ModelSerializer):
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


class BlogArticleDetailSerializer(ModelSerializer):

    class Meta:
        model = BlogArticle
        fields = ['id', 'title', 'intro', 'description',
                  'created_at', 'tags', 'author',  'image',
                  ]


class CommentSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Blogs:comment_detail_update_delete", read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'name', 'description', "blog_article",'created_at', "url")


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'name', 'description', "blog_article", 'created_at')


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


class NewsArticleDetailSerializer(ModelSerializer):

    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'intro', 'description', 'created_at',
                  'category', 'author', 'image'
                  ]

#
# class NewsCommentSerializer(ModelSerializer):
#     news_article = NewsArticleSerializer(read_only=True)
#
#     class Meta:
#         model = NewsComment
#         fields = ['id', 'name', 'description', 'news_article', 'created_at']


# GALLERY


class GallerySerializer(ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['id', 'image', 'text']


# NEWSLETTER


class NewsLetterSubscriptionSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Blogs:newsletter_subscription_detail_update", read_only=True)

    class Meta:
        model = NewsLetterSubscription
        fields = ('id', 'email', 'url')


class NewsLetterSubscriptionDetailSerializer(ModelSerializer):

    class Meta:
        model = NewsLetterSubscription
        fields = ('id', 'email', )


class CategorySerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Blogs:category_detail_update_delete", read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', "url"]


class CategoryDetailSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TagSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Blogs:tag_detail_update_delete", read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'url']


class TagDetailSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', ]


class NewsLetterSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="Blogs:newsletter_details_update_delete", read_only=True)

    class Meta:
        model = NewsLetter
        fields = (
            "id",
            "title",
            "content",
            "subject",
            "url"
        )


class NewsLetterDetailSerializer(ModelSerializer):

    class Meta:
        model = NewsLetter
        fields = (
            "id",
            "title",
            "content",
            "subject"
        )
