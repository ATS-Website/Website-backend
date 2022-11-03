from django.shortcuts import render
from Blogs.models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .mixins import AdminOrReadOnlyMixin
from .permissions import IsAdminOrReadOnly
from Blogs.serializers import *
import datetime


class BlogArticleListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
   queryset= BlogArticle.active_objects.all()
   serializer_class= BlogArticleSerializer

class BlogArticleRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
   queryset= BlogArticle.active_objects.all()
   serializer_class= BlogArticleSerializer
   lookup_field= "pk"


@api_view(['DELETE'])
def article_delete(request, pk):
   article_delete= BlogArticle.active_objects.get(pk=pk)
   article_delete.is_active=False
   article_delete.save()

   return Response('comment was deleted')


# COMMENTS
class CommentListCreateAPIView(generics.ListCreateAPIView):
   queryset= Comment.active_objects.all()
   serializer_class= CommentSerializer

@api_view(['DELETE'])
def comment_delete(request, pk):
   comment_delete= Comment.active_objects.get(pk=pk)
   comment_delete.is_active=False
   comment_delete.save()

   return Response('comment was deleted')


# AUTHOR
class AuthorListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
   queryset= Author.objects.all()
   serializer_class= AuthorSerializer


class AuthorRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
   queryset= Author.objects.all()
   serializer_class= AuthorSerializer
   lookup_field= "pk"


@api_view(['DELETE'])
def author_delete(request, pk):
   author= Author.objects.get(pk=pk)
   author.is_active=False
   author.save()

   return Response('author was deleted')

# author restore

# NEWS
class NewsArticleListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
   queryset= NewsArticle.active_objects.all()
   serializer_class= NewsArticleSerializer

class NewsArticleRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
   queryset= NewsArticle.objects.all()
   serializer_class= NewsArticleSerializer
   lookup_field= "pk"


@api_view(['DELETE'])
def news_delete(request, pk):
   news= NewsArticle.active_objects.get(pk=pk)
   news.is_active=False
   news.save()

   return Response('news was deleted')


# NEWSCOMMENT
class NewsCommentListCreateAPIView(generics.ListCreateAPIView):
   queryset= NewsComment.active_objects.all()[:10]
   serializer_class= NewsCommentSerializer


@api_view(['DELETE'])
def newscomment_delete(request, pk):
   newscomment_delete= NewsComment.active_objects.get(pk=pk)
   newscomment_delete.is_active=False
   newscomment_delete.save()

   return Response('newscomment was deleted')


# Gallery
class GalleryListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
   queryset= Gallery.objects.all()
   serializer_class= GallerySerializer

class GalleryRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
   queryset= Gallery.objects.all()
   serializer_class= GallerySerializer
   lookup_field= "pk"

@api_view(['DELETE'])
def gallery_delete(request, pk):
   gallery= Gallery.objects.get(pk=pk)
   gallery.is_active=False
   gallery.save()

   return Response('Gallery was deleted')


# Newsletter
class NewsLetterSubscriptionListCreateAPIView(generics.ListCreateAPIView):
   queryset= NewsLetterSubscription.objects.all()
   serializer_class= NewsLetterSubscriptionSerializer

class NewsLetterSubscriptionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
   queryset= NewsLetterSubscription.objects.all()
   serializer_class= NewsLetterSubscriptionSerializer
   lookup_field= "pk"


@api_view(['DELETE'])
def newslettersubscription_delete(request, pk):
   newsLetter= NewsLetterSubscription.objects.get(pk=pk)
   newsLetter.is_active=False
   newsLetter.save()

   return Response('Subscription was deleted')
