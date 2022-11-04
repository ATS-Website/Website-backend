from algoliasearch_django import raw_search
from django.shortcuts import render
from Blogs.models import *
<<<<<<< HEAD
from rest_framework.decorators import api_view, permission_classes
=======
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework import status
from .mixins import AdminOrReadOnlyMixin
from .permissions import IsAdminOrReadOnly
<<<<<<< HEAD
from rest_framework.permissions import IsAdminUser
from Blogs.serializers import *


class BlogListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
   queryset= Blog.active_objects.all()
   serializer_class= BlogSerializer

class BlogRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
   queryset= Blog.active_objects.all()
   serializer_class= BlogSerializer
   lookup_field= "pk"


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def blog_delete(request, pk):
   blog_delete= Blog.active_objects.get(pk=pk)
   blog_delete.is_active=False
   blog_delete.save()
=======
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


class BlogArticleListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


class BlogArticleRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
    queryset = BlogArticle.active_objects.all()
    serializer_class = BlogArticleSerializer
    renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
def article_delete(request, pk):
    article_delete = BlogArticle.active_objects.get(pk=pk)
    article_delete.is_active = False
    article_delete.save()
>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3

    return Response({"message": 'Article was deleted'}, status=status.HTTP_204_NO_CONTENT)


# COMMENTS
<<<<<<< HEAD
class BlogCommentListCreateAPIView(generics.ListCreateAPIView):
   queryset= BlogComment.active_objects.all()
   serializer_class= BlogCommentSerializer

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def blogcomment_delete(request, pk):
   blogcomment_delete= BlogComment.active_objects.get(pk=pk)
   blogcomment_delete.is_active=False
   blogcomment_delete.save()
=======
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
>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3

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
<<<<<<< HEAD
@permission_classes([IsAdminUser])
=======
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3
def author_delete(request, pk):
    author = Author.objects.get(pk=pk)
    author.is_active = False
    author.save()

    return Response({"message": 'Author was deleted'}, status=status.HTTP_204_NO_CONTENT)


# author restore

# NEWS
<<<<<<< HEAD
class NewsListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
   queryset= News.active_objects.all()
   serializer_class= NewsSerializer

class NewsRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
   queryset= News.active_objects.all()
   serializer_class= NewsSerializer
   lookup_field= "pk"


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def news_delete(request, pk):
   news= News.active_objects.get(pk=pk)
   news.is_active=False
   news.save()
=======


class NewsArticleListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleSerializer
    renderer_classes = [CustomRenderer]


class NewsArticleRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
    queryset = NewsArticle.active_objects.all()
    serializer_class = NewsArticleSerializer
    renderer_classes = [CustomRenderer]
    lookup_field = "pk"


@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
def news_delete(request, pk):
    news = NewsArticle.active_objects.get(pk=pk)
    news.is_active = False
    news.save()
>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3

    return Response({"message": 'News was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


# NEWSCOMMENT
class NewsCommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = NewsComment.active_objects.all()[:10]
    renderer_classes = [CustomRenderer]
    serializer_class = NewsCommentSerializer


@api_view(['DELETE'])
<<<<<<< HEAD
@permission_classes([IsAdminUser])
def newscomment_delete(request, pk):
   newscomment_delete= NewsComment.active_objects.get(pk=pk)
   newscomment_delete.is_active=False
   newscomment_delete.save()
=======
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
def newscomment_delete(request, news_pk, pk):
    newscomment = NewsComment.active_objects.get(
        news_article=news_pk, pk=pk)
    newscomment.is_active = False
    newscomment.save()
>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3

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
<<<<<<< HEAD
@permission_classes([IsAdminUser])
=======
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3
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
<<<<<<< HEAD
@permission_classes([IsAdminUser])
=======
@permission_classes([permissions.IsAdminUser])
@renderer_classes(CustomRenderer,)
>>>>>>> 59e03d11622229baf448dbe28231a65516555ef3
def newslettersubscription_delete(request, pk):
    newsLetter = NewsLetterSubscription.objects.get(pk=pk)
    newsLetter.is_active = False
    newsLetter.save()

    return Response({"message": 'The Subscription was sucessfully annulled'}, status=status.HTTP_204_NO_CONTENT)
