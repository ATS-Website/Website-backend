from algoliasearch_django import raw_search
from django.shortcuts import render
from Blogs.models import *
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework import status
from .mixins import AdminOrReadOnlyMixin
from .permissions import IsAdminOrReadOnly
from .serializers import *
from .paginations import ResponsePagination
from Accounts.renderers import CustomRenderer
import datetime
from . import client


class SearchBlogView(generics.ListAPIView):
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        # tag = request.GET.get("tag") or None
        if not query:
            return Response({"message": "An Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)

        params = {"hitsPerPage": 5}
        results = raw_search(BlogArticle, query, params)

        # results = client.perform_search(query)
        return Response(results, status=status.HTTP_200_OK)


class SearchNewsView(generics.ListAPIView):
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        # tag = request.GET.get("tag") or None
        if not query:
            return Response({"message": "An Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)

        params = {"hitsPerPage": 5}
        results = raw_search(NewsArticle, query, params)
        return Response(results, status=status.HTTP_200_OK)


class BlogArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class BlogArticleRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes(CustomRenderer,)
# def blog_delete(request, pk):
#     blog_delete = BlogArticle.active_objects.get(pk=pk)
#     blog_delete.is_active = False
#     blog_delete.save()

#     return Response({"message": 'Blog was deleted'}, status=status.HTTP_204_NO_CONTENT)


# COMMENTS
class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.active_objects.all()
    serializer_class = CommentSerializer
    renderer_classes = [CustomRenderer]


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
def comment_delete(request, blog_pk, pk):
    comment = Comment.active_objects.get(blog_article__pk=blog_pk, pk=pk)
    comment.is_active = False
    comment.save()

    return Response({"message": 'comment was deleted'}, status=status.HTTP_204_NO_CONTENT)


# AUTHOR
class AuthorListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    renderer_classes = [CustomRenderer]


class AuthorRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = "pk"


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
def author_delete(request, pk):
    author = Author.objects.get(pk=pk)
    author.is_active = False
    author.save()

    return Response({"message": 'Author was deleted'}, status=status.HTTP_204_NO_CONTENT)


# author restore

# NEWS

class NewsArticleListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleSerializer
    renderer_classes = [CustomRenderer,BrowsableAPIRenderer]


class NewsArticleRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return super().delete(request, *args, **kwargs)


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes(CustomRenderer,)
# def news_delete(request, pk):
#     news = NewsArticle.active_objects.get(pk=pk)
#     news.is_active = False
#     news.save()

#     return Response({"message": 'News was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


# NEWSCOMMENT
class NewsCommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = NewsComment.active_objects.all()
    renderer_classes = [CustomRenderer]
    serializer_class = NewsCommentSerializer


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
def newscomment_delete(request, news_pk, pk):
    newscomment = NewsComment.active_objects.get(
        news_article=news_pk, pk=pk)
    newscomment.is_active = False
    newscomment.save()

    return Response({"message": 'The Comment on the New was sucessfully deleted'}, status=status.HTTP_204_NO_CONTENT)


# Gallery
class GalleryListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class GalleryRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    lookup_field = "pk"


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
def gallery_delete(request, pk):
    gallery = Gallery.objects.get(pk=pk)
    gallery.is_active = False
    gallery.save()

    return Response({"message": 'The Image was sucessfully deleted'}, status=status.HTTP_204_NO_CONTENT)

# Newsletter


class NewsLetterSubscriptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionSerializer
    renderer_classes = [CustomRenderer, ]


class NewsLetterSubscriptionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionSerializer
    renderer_classes = [CustomRenderer, ]
    lookup_field = "pk"


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
def newslettersubscription_delete(request, pk):
    newsLetter = NewsLetterSubscription.objects.get(pk=pk)
    newsLetter.is_active = False
    newsLetter.save()

    return Response({"message": 'The Subscription was sucessfully annulled'}, status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(AdminOrReadOnlyMixin, generics. ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = [CustomRenderer,]
    lookup_field = "pk"


class TagListCreateAPIView(AdminOrReadOnlyMixin, generics. ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    renderer_classes = [CustomRenderer,]
    lookup_field = "pk"