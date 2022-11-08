import datetime
from algoliasearch_django import raw_search
from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from Accounts.renderers import CustomRenderer

from Tech_Stars.mixins import (CustomRetrieveUpdateDestroyAPIView, CustomListCreateAPIView,
                               CustomRetrieveUpdateAPIView, CustomCreateAPIView
                               )

from .mixins import AdminOrReadOnlyMixin
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


class BlogArticleListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class BlogArticleRetrieveUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleDetailSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes(CustomRenderer,)
# def blog_delete(request, pk):
#     blog_delete = BlogArticle.active_objects.get(pk=pk)
#     blog_delete.is_active = False
#     blog_delete.save()

#     return Response({"message": 'Blog was deleted'}, status=status.HTTP_204_NO_CONTENT)


# COMMENTS
class CommentListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentSerializer
    renderer_classes = [CustomRenderer]


class CommentDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentDetailSerializer
    renderer_classes = (CustomRenderer,)


# AUTHOR
class AuthorListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    renderer_classes = [CustomRenderer]


class AuthorRetrieveUpdateAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDetailSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = "pk"


# NEWS

class NewsArticleListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class NewsArticleRetrieveUpdateDeleteAPIView(CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleDetailSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = "pk"


# Gallery
class GalleryListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class GalleryRetrieveUpdateAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    lookup_field = "pk"


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes(CustomRenderer, )
# def gallery_delete(request, pk):
#     gallery = Gallery.objects.get(pk=pk)
#     gallery.is_active = False
#     gallery.save()
#
#     return Response({"message": 'The Image was sucessfully deleted'}, status=status.HTTP_204_NO_CONTENT)


# Newsletter


class NewsLetterSubscriptionListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionSerializer
    renderer_classes = [CustomRenderer, ]


class NewsLetterSubscriptionRetrieveUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionDetailSerializer
    renderer_classes = [CustomRenderer, ]
    lookup_field = "pk"


class SendNewsLetter(APIView):
    def get_object(self):
        return list(NewsLetterSubscription.active_objects.all())

    def post(self, request, *args, **kwargs):
        try:
            news_letter = NewsLetter.active_objects.get(id=kwargs["pk"])
        except:
            raise ValidationError("NewsLetter does not exist !")

        new_send_mail_func(vars(news_letter), self.get_object())

        return Response("Messages Sent Successfully", status=HTTP_201_CREATED)


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes(CustomRenderer, )
# def newslettersubscription_delete(request, pk):
#     newsLetter = NewsLetterSubscription.objects.get(pk=pk)
#     newsLetter.is_active = False
#     newsLetter.save()
#
#     return Response({"message": 'The Subscription was sucessfully annulled'}, status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Category.active_objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [CustomRenderer, ]
    lookup_field = "pk"


class CategoryDetailUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Category.active_objects.all()
    serializer_class = CategoryDetailSerializer
    renderer_classes = (CustomRenderer,)


class TagListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Tag.active_objects.all()
    serializer_class = TagSerializer
    renderer_classes = [CustomRenderer, ]
    lookup_field = "pk"


class TagDetailUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Tag.active_objects.all()
    serializer_class = TagDetailSerializer
    renderer_classes = (CustomRenderer,)


class NewsLetterListCreateAPIView(AdminOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsLetter.active_objects.all()
    serializer_class = NewsLetterSerializer
    renderer_classes = (CustomRenderer,)


class NewsLetterDetailsUpdateDeleteAPIView(AdminOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetter.active_objects.all()
    serializer_class = NewsLetterDetailSerializer
    renderer_classes = (CustomRenderer, )
