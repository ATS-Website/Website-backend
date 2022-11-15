import datetime
import itertools

from algoliasearch_django import raw_search
from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, FileUploadParser, MultiPartParser

from Accounts.renderers import CustomRenderer
from Accounts.permissions import IsValidRequestAPIKey

from Tech_Stars.mixins import (CustomRetrieveUpdateDestroyAPIView, CustomListCreateAPIView,
                               CustomRetrieveUpdateAPIView, CustomCreateAPIView
                               )

from .mixins import AdminOrContentManagerOrReadOnlyMixin
from .permissions import IsAdminOrReadOnly
from .serializers import *
from .paginations import ResponsePagination

from .models import *
from . import client
from .utils import new_send_mail_func


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


class BlogArticleListCreateAPIView (AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class BlogArticleRetrieveUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleDetailSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


# COMMENTS
class CommentListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentSerializer
    renderer_classes = [CustomRenderer]


class CommentDetailsUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentDetailSerializer
    renderer_classes = (CustomRenderer,)


# AUTHOR
class AuthorListCreateAPIView( CustomListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    renderer_classes = [CustomRenderer]


class AuthorRetrieveUpdateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = "pk"


# NEWS

class NewsArticleListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class NewsArticleRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleDetailSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
    # lookup_field = "pk"


# Gallery
class GalleryListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Gallery.active_objects.all()
    renderer_classes = [CustomRenderer]
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = GallerySerializer


class GalleryRetrieveUpdateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateAPIView):
    queryset = Gallery.active_objects.all()
    renderer_classes = [CustomRenderer]
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = GallerySerializer
    lookup_field = "pk"


class NewsLetterSubscriptionListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionSerializer
    renderer_classes = [CustomRenderer, ]


class NewsLetterSubscriptionRetrieveUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin,
                                                        CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionDetailSerializer
    renderer_classes = [CustomRenderer, ]
    lookup_field = "pk"


class SendNewsLetter(AdminOrContentManagerOrReadOnlyMixin, APIView):
    def get_object(self):
        return [x.email for x in NewsLetterSubscription.active_objects.all()]

    def post(self, request, *args, **kwargs):
        try:
            news_letter = NewsLetter.active_objects.get(id=kwargs["pk"])
        except:
            raise ValidationError("NewsLetter does not exist !")

        new_send_mail_func(vars(news_letter), self.get_object())

        return Response("Messages Sent Successfully", status=HTTP_201_CREATED)


class CategoryListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Category.active_objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [CustomRenderer, ]
    lookup_field = "pk"


class CategoryDetailUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Category.active_objects.all()
    serializer_class = CategoryDetailSerializer
    renderer_classes = (CustomRenderer, BrowsableAPIRenderer)


# class TagListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
#     queryset = Tag.active_objects.all()
#     serializer_class = TagSerializer
#     renderer_classes = [CustomRenderer, ]
#     lookup_field = "pk"


# class TagDetailUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
#     queryset = Tag.active_objects.all()
#     serializer_class = TagDetailSerializer
#     renderer_classes = (CustomRenderer,)


class NewsLetterListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsLetter.active_objects.all()
    serializer_class = NewsLetterSerializer
    renderer_classes = (CustomRenderer,)


class NewsLetterDetailsUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetter.active_objects.all()
    serializer_class = NewsLetterDetailSerializer
    renderer_classes = (CustomRenderer,)


class BlogArticleCommentListAPIView(APIView):
    renderer_classes = (CustomRenderer,)

    def get(self, request,  *args, **kwargs):
        queryset = Comment.active_objects.filter(blog_article_id=kwargs["pk"])
        serializer = CommentSerializer(
            queryset, many=True, context={"request": request})
        return Response(serializer.data, status=HTTP_200_OK)


class ViewsListCreateAPIView(CreateAPIView):
    queryset = Views.active_objects.all()
    serializer_class = BlogViewsSerializer
    renderer_classes = (CustomRenderer,)


class LikesCreateAPIView(CreateAPIView):
    serializer_class = LikeSerializer
    renderer_classes = (CustomRenderer,)
    queryset = Likes.active_objects.all()


class CategoryNewsCountAPIView(APIView):
    renderer_classes = (CustomRenderer,)

    def get(self, request, *args, **kwargs):
        queryset = Category.active_objects.all()[:6]
        serializer = CategoryNewsCountSerializer(queryset, many=True, )
        return Response(serializer.data, status=HTTP_200_OK)
