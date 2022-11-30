from .documents import NewsArticleDocument, BlogArticleDocument

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from django.core.validators import validate_image_file_extension
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, ListField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *


class SearchBlogSerializer(ModelSerializer):
    class Meta:
        model = BlogArticle
        fields = ('id', 'title', 'intro', 'description')


class SearchBlogSerializer(ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ('id', 'title', 'intro', 'description')


class NewsArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = NewsArticleDocument

        fields = (
            'title',
            'intro',
            'description',
            'category',
            'author'
        )


class BlogArticleDocumentSerializer(DocumentSerializer):
    class Meta:
        document = BlogArticleDocument

        fields = (
            'title',
            'intro',
            'description',
            'author'
        )


class AuthorSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="blogs:author_detail_update", read_only=True)

    class Meta:
        model = Author
        fields = ['id',
                  'first_name', 'last_name', 'email',
                  'bio', 'profile_pics', "url", "twitter_link", "facebook_link", "instagram_link"
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
                  'created_at', 'author', 'url', 'image', "min_read", "author_fullname", "author_image",
                  ]
        extra_kwargs = {
            "author": {"write_only": True}
        }

    def get_url(self, obj):
        return self.context.get("request").build_absolute_uri("/api/v1/blogs/") + str(obj.pk)


class CommentSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="blogs:comment_detail_update_delete", read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'name', 'description',
                  "blog_article", 'created_at', "url")


class BlogArticleDetailSerializer(ModelSerializer):
    more_comments = HyperlinkedIdentityField(
        view_name="blogs:blog_comments", read_only=True)
    few_comments = CommentSerializer(read_only=True, many=True)
    author = AuthorDetailSerializer()

    class Meta:
        model = BlogArticle
        fields = ['id', 'title', 'description',
                  'created_at', 'author', 'image', "likes_count", "comment_count", "views_count",
                  "min_read", "author_fullname", "few_comments", "more_comments", ]


class CommentDetailSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'description', "blog_article", 'created_at')


class CategorySerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="blogs:category_detail_update_delete", read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', "url"]


class CategoryDetailSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# NEWS SERIALIZER


class NewsArticleSerializer(ModelSerializer):
    url = serializers.SerializerMethodField()
    author_name = serializers.CharField(read_only=True)
    category_name = serializers.CharField(
        read_only=True)

    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'intro', 'description', 'created_at',
                  'category', 'author', 'image', 'url', 'author_name', "category_name", "author_image"
                  ]

    def get_url(self, obj):
        return self.context.get("request").build_absolute_uri("/api/v1/news/") + str(obj.pk)


class NavNewsSerializer(ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = ("category_name", "title")


class NewsArticleDetailSerializer(ModelSerializer):
    author = AuthorDetailSerializer()
    category = CategoryDetailSerializer()

    class Meta:
        model = NewsArticle
        fields = ['id', 'title', 'intro', 'description', 'created_at',
                  'category', 'author', 'image'
                  ]


# NEWSLETTER


class NewsLetterSubscriptionSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="blogs:newsletter_subscription_detail_update", read_only=True)

    class Meta:
        model = NewsLetterSubscription
        fields = ('id', 'email', 'url')


class NewsLetterSubscriptionDetailSerializer(ModelSerializer):
    class Meta:
        model = NewsLetterSubscription
        fields = ('id', 'email',)


# class TagSerializer(ModelSerializer):
#     url = HyperlinkedIdentityField(
#         view_name="blogs:tag_detail_update_delete", read_only=True)
#
#     class Meta:
#         model = Tag
#         fields = ['id', 'name', 'url']

#
# class TagDetailSerializer(ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ['id', 'name', ]


class NewsLetterSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="blogs:newsletter_details_update_delete", read_only=True)

    class Meta:
        model = NewsLetter
        fields = (
            "id",
            "title",
            "content",
            "trunc_content",
            "subject",
            "url"
        )

        extra_kwargs = {
            "content": {"write_only": True}
        }


class NewsLetterDetailSerializer(ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = (
            "id",
            "title",
            "content",
            "subject"
        )


class BlogViewsSerializer(ModelSerializer):
    class Meta:
        model = Views
        fields = (
            "blog_article",
            "viewer_ip"
        )

    def create(self, validated_data):
        blog_article = validated_data.get("blog_article")
        ip = validated_data.get("viewer_ip")
        view = Views.active_objects.get_or_create(
            blog_article=BlogArticle.active_objects.get(id=blog_article.id))[0]

        if ip not in view.viewer_ip:
            view.viewer_ip.append(ip)
            view.save()
            return view


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Likes
        fields = (
            "blog_article",
            "ip_address"
        )

    def create(self, validated_data):
        blog_article = validated_data.get("blog_article")
        ip = validated_data.get("ip_address")

        view = Likes.active_objects.get_or_create(
            blog_article=BlogArticle.active_objects.get(id=blog_article.id))[0]

        if ip not in view.ip_address:
            view.ip_address.append(ip)
        else:
            view.ip_address.remove(ip)

        view.save()
        return view


class CategoryNewsCountSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "category_news_count"
        )


class ImagesSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = ("image", "alt", "date_created")


class AlbumSerializer(ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)
    url = HyperlinkedIdentityField(
        view_name="blogs:album_retrieve_update_delete", read_only=True)

    class Meta:
        model = Album
        fields = ("name", "description", "images", "url")

    def create(self, validated_data):
        images = self.context.get("view").request.FILES
        name = validated_data.get("name")
        description = validated_data.get("description")
        album = Album.active_objects.get_or_create(name=name, description=description)[0]

        for image in images.values():
            if image.size > 10000000:
                continue
            try:
                validate_image_file_extension(image)
                Images.active_objects.create(image=image, album=album)
            except Exception as e:
                pass

        if album.active_images.count() < 1:
            album.delete()
            raise ValidationError("Invalid Picture(s)")

        return album


class AlbumDetailSerializer(ModelSerializer):
    active_images = ImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = (
            "name",
            "description",
            "active_images"
        )


class VisitorsSerializer(ModelSerializer):
    class Meta:
        model = Visitors
        fields = ("ip_address",)

    def create(self, validated_data):
        visitor = Visitors.objects.all().first()
        ip_address = validated_data.get("ip_address")
        if visitor is None:
            new_visitor = Visitors.objects.create()
            new_visitor.ip_address.append(ip_address)
            new_visitor.save()
            return new_visitor
        if ip_address not in visitor.ip_address:
            visitor.ip_address.append(ip_address)
            visitor.save()
        return visitor
