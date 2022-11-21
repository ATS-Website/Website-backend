import datetime
import itertools
import json

from django.forms.models import model_to_dict

from algoliasearch_django import raw_search
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, FileUploadParser, MultiPartParser

from Accounts.renderers import CustomRenderer
from Accounts.permissions import IsValidRequestAPIKey

from Tech_Stars.mixins import (CustomRetrieveUpdateDestroyAPIView, CustomListCreateAPIView,
                               CustomRetrieveUpdateAPIView
                               )

from .mixins import AdminOrContentManagerOrReadOnlyMixin
from .serializers import *

from .models import *
from . import client
from .tasks import new_send_mail_func


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


# COMMENTS
class CommentListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentSerializer


class CommentDetailsUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentDetailSerializer


# AUTHOR
class AuthorListCreateAPIView(CustomListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorRetrieveUpdateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer


# NEWS

class NewsArticleListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleSerializer


class NewsArticleRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleDetailSerializer


class NewsLetterSubscriptionListCreateAPIView(CustomListCreateAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionSerializer


class NewsLetterSubscriptionRetrieveUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin,
                                                        CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetterSubscription.objects.all()
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
        # print(model_to_dict(news_letter))
        # print([x.email for x in NewsLetterSubscription.active_objects.all()])
        # print({x.email: x.email for x in NewsLetterSubscription.active_objects.all()})
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


class AlbumListCreateAPIView(CustomListCreateAPIView):
    queryset = Album.active_objects.all()
    serializer_class = AlbumSerializer
    parser_classes = (MultiPartParser, FormParser)


class AlbumRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = Album.active_objects.all()
    serializer_class = AlbumDetailSerializer
    parser_classes = (MultiPartParser, FormParser)


class NavNewsListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = NewsArticle.active_objects.all()
        serializer = NavNewsSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
