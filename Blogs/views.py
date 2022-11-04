from django.shortcuts import render
from Blogs.models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .mixins import AdminOrReadOnlyMixin
from .permissions import IsAdminOrReadOnly
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

   return Response('comment was deleted')


# COMMENTS
class BlogCommentListCreateAPIView(generics.ListCreateAPIView):
   queryset= BlogComment.active_objects.all()
   serializer_class= BlogCommentSerializer

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def blogcomment_delete(request, pk):
   blogcomment_delete= BlogComment.active_objects.get(pk=pk)
   blogcomment_delete.is_active=False
   blogcomment_delete.save()

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
@permission_classes([IsAdminUser])
def author_delete(request, pk):
   author= Author.objects.get(pk=pk)
   author.is_active=False
   author.save()

   return Response('author was deleted')

# author restore

# NEWS
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

   return Response('news was deleted')


# NEWSCOMMENT
class NewsCommentListCreateAPIView(generics.ListCreateAPIView):
   queryset= NewsComment.active_objects.all()[:10]
   serializer_class= NewsCommentSerializer


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
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
@permission_classes([IsAdminUser])
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
@permission_classes([IsAdminUser])
def newslettersubscription_delete(request, pk):
   newsLetter= NewsLetterSubscription.objects.get(pk=pk)
   newsLetter.is_active=False
   newsLetter.save()

   return Response('Subscription was deleted')
