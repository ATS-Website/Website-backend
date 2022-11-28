import datetime
import itertools
import json
from blogs.permissions import IsAdminOrReadOnly
from django.forms.models import model_to_dict
from django.utils import timezone

from algoliasearch_django import raw_search
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK

from rest_framework.parsers import FormParser, FileUploadParser, MultiPartParser

from accounts.renderers import CustomRenderer
from accounts.permissions import IsValidRequestAPIKey

from tech_stars.mixins import (
    CustomRetrieveUpdateDestroyAPIView, CustomListCreateAPIView, CustomDestroyAPIView)

from .mixins import AdminOrContentManagerOrReadOnlyMixin
from .serializers import *

from .models import *
from . import client
from .tasks import new_send_mail_func



from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, SuggesterFilterBackend
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from .documents import NewsArticleDocument
from .serializers import NewsArticleDocumentSerializer


class NewsArticleDocumentView(DocumentViewSet):
    document = NewsArticleDocument
    serializer_class = NewsArticleDocumentSerializer

    filter_backends = [SearchFilterBackend]
    search_fields = ('title', "intro", "description", "category")
    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'description': {
            'field': 'description.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'intro': {
            'field': 'intro.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'category': {
            'field': 'category.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }


class BlogArticleDocumentView(DocumentViewSet):
    document = BlogArticleDocument
    serializer_class = BlogArticleDocumentSerializer

    filter_backends = [SearchFilterBackend, SuggesterFilterBackend]
    search_fields = ('title', "intro", "description", "author")
    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'description': {
            'field': 'description.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'intro': {
            'field': 'intro.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'author': {
            'field': 'author.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }


class SearchBlogView(generics.ListAPIView):
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        # tag = request.GET.get("tag") or None
        if not query:
            return Response({"message": "An Error Occurred"}, status=HTTP_400_BAD_REQUEST)

        params = {"hitsPerPage": 5}
        results = raw_search(BlogArticle, query, params)

        # results = client.perform_search(query)
        return Response(results, status=HTTP_200_OK)


class SearchNewsView(generics.ListAPIView):
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        # tag = request.GET.get("tag") or None
        if not query:
            return Response({"message": "An Error Occurred"}, status=HTTP_400_BAD_REQUEST)

        params = {"hitsPerPage": 5}
        results = raw_search(NewsArticle, query, params)
        return Response(results, status=HTTP_200_OK)


class BlogArticleListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class BlogArticleRetrieveUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleDetailSerializer


class TrashedBlogListAPIView(IsAdminOrReadOnly, ListAPIView):
    queryset = BlogArticle.Inactive_objects.all()
    serializer_class = BlogArticleSerializer


class TrashedBlogRestoreAPIView(IsAdminOrReadOnly, CustomDestroyAPIView):
    queryset = BlogArticle.Inactive_objects.all()
    serializer_class = BlogArticleDetailSerializer


# COMMENTS
class CommentListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentSerializer


class CommentDetailsUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentDetailSerializer


class TrashedCommentListAPIView(IsAdminOrReadOnly, ListAPIView):
    queryset = Comment.inactive_objects.all()
    serializer_class = CommentSerializer


class TrashedCommentRestoreAPIView(IsAdminOrReadOnly, CustomDestroyAPIView):
    queryset = Comment.inactive_objects.all()
    serializer_class = CommentSerializer


# AUTHOR
class AuthorListCreateAPIView(CustomListCreateAPIView):
    queryset = Author.active_objects.all()
    serializer_class = AuthorSerializer


class AuthorRetrieveUpdateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Author.active_objects.all()
    serializer_class = AuthorDetailSerializer


class TrashedAuthorListAPIView(IsAdminOrReadOnly, ListAPIView):
    queryset = Author.Inactive_objects.all()
    serializer_class = AuthorSerializer


class TrashedAuthorRestoreAPIView(IsAdminOrReadOnly, CustomDestroyAPIView):
    queryset = Author.Inactive_objects.all()
    serializer_class = AuthorDetailSerializer


# NEWS

class NewsArticleListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleSerializer


class NewsArticleRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleDetailSerializer


class TrashedNewsListAPIView(IsAdminOrReadOnly, ListAPIView):
    queryset = NewsArticle.inactive_objects.all()
    serializer_class = NewsArticleSerializer


class TrashedNewsRestoreAPIView(IsAdminOrReadOnly, CustomDestroyAPIView):
    queryset = NewsArticle.inactive_objects.all()
    serializer_class = NewsArticleDetailSerializer


class NewsLetterSubscriptionListCreateAPIView(CustomListCreateAPIView):
    queryset = NewsLetterSubscription.active_objects.all()
    serializer_class = NewsLetterSubscriptionSerializer


class NewsLetterSubscriptionRetrieveUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin,
                                                        CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetterSubscription.active_objects.all()
    serializer_class = NewsLetterSubscriptionDetailSerializer


class SendNewsLetter(AdminOrContentManagerOrReadOnlyMixin, APIView):
    renderer_classes = [CustomRenderer]

    def get_object(self):
        return {x.email: x.email for x in NewsLetterSubscription.active_objects.all()}

    def post(self, request, *args, **kwargs):
        try:
            news_letter = NewsLetter.active_objects.get(id=kwargs["pk"])
        except:
            raise ValidationError("NewsLetter does not exist !")

        new_send_mail_func.delay(model_to_dict(news_letter), self.get_object())

        return Response("Messages Sent Successfully", status=HTTP_201_CREATED)


class CategoryListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Category.active_objects.all()
    serializer_class = CategorySerializer


class CategoryDetailUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Category.active_objects.all()
    serializer_class = CategoryDetailSerializer


class NewsLetterListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsLetter.active_objects.all()
    serializer_class = NewsLetterSerializer


class NewsLetterDetailsUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetter.active_objects.all()
    serializer_class = NewsLetterDetailSerializer


class BlogArticleCommentListAPIView(APIView):
    renderer_classes = (CustomRenderer,)

    def get(self, request, *args, **kwargs):
        queryset = Comment.active_objects.filter(blog_article_id=kwargs["pk"])
        serializer = CommentSerializer(
            queryset, many=True, context={"request": request})
        return Response(serializer.data, status=HTTP_200_OK)


class ViewsListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CreateAPIView):
    queryset = Views.active_objects.all()
    serializer_class = BlogViewsSerializer


class LikesCreateAPIView(CreateAPIView):
    serializer_class = LikeSerializer
    queryset = Likes.active_objects.all()


class CategoryNewsCountAPIView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Category.active_objects.all()[:6]
        serializer = CategoryNewsCountSerializer(queryset, many=True, )
        return Response(serializer.data, status=HTTP_200_OK)


class ImageListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Images.active_objects.all()
        serializer = ImagesSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class TrashedImageListAPIView(AdminOrContentManagerOrReadOnlyMixin, ListAPIView):
    queryset = Images.inactive_objects.all()
    serializer_class = ImagesSerializer


class TrashedImageRestoreAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomDestroyAPIView):
    queryset = Images.inactive_objects.all()
    serializer_class = ImagesSerializer


class AlbumListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Album.active_objects.all()
    serializer_class = AlbumSerializer
    parser_classes = (MultiPartParser, FormParser)


class AlbumRetrieveUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Album.active_objects.all()
    serializer_class = AlbumDetailSerializer
    parser_classes = (MultiPartParser, FormParser)


class NavNewsListAPIView(AdminOrContentManagerOrReadOnlyMixin, APIView):
    def get(self, request, *args, **kwargs):
        queryset = NewsArticle.active_objects.all()
        serializer = NavNewsSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class VisitorListCreateView(AdminOrContentManagerOrReadOnlyMixin, CreateAPIView):
    queryset = Visitors.objects.all()
    serializer_class = VisitorsSerializer


class UpdatesNumbersListView(AdminOrContentManagerOrReadOnlyMixin, APIView):
    def get(self, request, *args, **kwargs):
        total_visitors = len(Visitors.objects.all().first().ip_address)
        total_blogs = BlogArticle.active_objects.all()
        total_news = NewsArticle.active_objects.all()
        latest_blogs = total_blogs.filter(created_at__gte=(timezone.now() - timezone.timedelta(days=14))).count()
        latest_news = total_news.filter(created_at__gte=(timezone.now() - timezone.timedelta(days=14))).count()

        data = {
            "total_visitors": total_visitors,
            "total_blogs": total_blogs.count(),
            "total_news": total_news.count(),
            "latest_post": latest_news + latest_blogs
        }
        return Response(data, status=HTTP_200_OK)
