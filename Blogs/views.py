import datetime
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

from Accounts.renderers import CustomRenderer

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


class BlogArticleListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
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
class AuthorListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
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
    renderer_classes = [CustomRenderer]
    lookup_field = "pk"


# Gallery
class GalleryListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Gallery.active_objects.all()
    renderer_classes = [CustomRenderer]
    serializer_class = GallerySerializer


class GalleryRetrieveUpdateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateAPIView):
    queryset = Gallery.active_objects.all()
    renderer_classes = [CustomRenderer]
    serializer_class = GallerySerializer
    lookup_field = "pk"


class NewsLetterSubscriptionListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionSerializer
    renderer_classes = [CustomRenderer, ]


class NewsLetterSubscriptionRetrieveUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetterSubscription.objects.all()
    serializer_class = NewsLetterSubscriptionDetailSerializer
    renderer_classes = [CustomRenderer, ]
    lookup_field = "pk"


class SendNewsLetter(AdminOrContentManagerOrReadOnlyMixin, APIView):
    def get_object(self):
        return list(NewsLetterSubscription.active_objects.all())

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
    renderer_classes = (CustomRenderer,)


class TagListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = Tag.active_objects.all()
    serializer_class = TagSerializer
    renderer_classes = [CustomRenderer, ]
    lookup_field = "pk"


class TagDetailUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = Tag.active_objects.all()
    serializer_class = TagDetailSerializer
    renderer_classes = (CustomRenderer,)


class NewsLetterListCreateAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomListCreateAPIView):
    queryset = NewsLetter.active_objects.all()
    serializer_class = NewsLetterSerializer
    renderer_classes = (CustomRenderer,)


class NewsLetterDetailsUpdateDeleteAPIView(AdminOrContentManagerOrReadOnlyMixin, CustomRetrieveUpdateDestroyAPIView):
    queryset = NewsLetter.active_objects.all()
    serializer_class = NewsLetterDetailSerializer
    renderer_classes = (CustomRenderer,)


class BlogArticleCommentListAPIView(APIView):
    def get(self, *args, **kwargs):
        queryset = Comment.active_objects.filter(blog_article_id=kwargs["pk"])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class ViewsListCreateAPIView(CreateAPIView):
    queryset = Views.active_objects.all()
    serializer_class = BlogViewsSerializer
    renderer_classes = (CustomRenderer,)


class LikesCreateAPIView(CreateAPIView):
    serializer_class = LikeSerializer
    renderer_classes = (CustomRenderer, )
    queryset = Likes.active_objects.all()


# from algoliasearch_django import raw_search
# from django.shortcuts import render, get_object_or_404
# from Blogs.models import *
# from rest_framework.renderers import BrowsableAPIRenderer
# from rest_framework.decorators import api_view, renderer_classes, permission_classes
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import generics, permissions
# from rest_framework import status
# from .mixins import AdminOrReadOnlyMixin
# from .permissions import IsAdminOrReadOnly
# from .serializers import *
# from .paginations import ResponsePagination
# from Accounts.renderers import CustomRenderer
# import datetime
# from . import client


# class SearchBlogView(generics.ListAPIView):
#     renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
#     serializer_class = SearchBlogSerializer

#     def get(self, request, *args, **kwargs):
#         query = request.GET.get("q")
#         # tag = request.GET.get("tag") or None
#         if not query:
#             return Response({"message": "An Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)

#         params = {"hitsPerPage": 5}
#         results = raw_search(BlogArticle, query, params)

#         # results = client.perform_search(query)
#         return Response(results, status=status.HTTP_200_OK)


# class SearchNewsView(generics.ListAPIView):
#     renderer_classes = [CustomRenderer, BrowsableAPIRenderer]

#     def get(self, request, *args, **kwargs):
#         query = request.GET.get("q")
#         # tag = request.GET.get("tag") or None
#         if not query:
#             return Response({"message": "An Error Occurred"}, status=status.HTTP_400_BAD_REQUEST)

#         params = {"hitsPerPage": 5}
#         results = raw_search(NewsArticle, query, params)
#         return Response(results, status=status.HTTP_200_OK)


# class BlogArticleListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
#     queryset = BlogArticle.active_objects.all()
#     serializer_class = BlogArticleSerializer
#     renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


# class BlogArticleRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
#     queryset = BlogArticle.active_objects.all()
#     serializer_class = BlogArticleSerializer
#     renderer_classes = [CustomRenderer, BrowsableAPIRenderer]


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes([CustomRenderer, ])
# def article_delete(request, pk):
#     article_delete = BlogArticle.active_objects.get(pk=pk)
#     article_delete.is_active = False
#     article_delete.save()

#     return Response({"message": 'Article was deleted'}, status=status.HTTP_204_NO_CONTENT)


# # COMMENTS
# class CommentListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Comment.active_objects.all()
#     serializer_class = CommentSerializer
#     renderer_classes = [CustomRenderer]


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes([CustomRenderer, ])
# def comment_delete(request, blog_pk, pk):
#     comment = Comment.active_objects.get(blog_article__pk=blog_pk, pk=pk)
#     comment.is_active = False
#     comment.save()

#     return Response({"message": 'comment was deleted'}, status=status.HTTP_204_NO_CONTENT)


# # AUTHOR
# class AuthorListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#     renderer_classes = [CustomRenderer]


# class AuthorRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#     renderer_classes = [CustomRenderer]
#     lookup_field = "pk"


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes([CustomRenderer, ])
# def author_delete(request, pk):
#     author = Author.objects.get(pk=pk)
#     author.is_active = False
#     author.save()

#     return Response({"message": 'Author was deleted'}, status=status.HTTP_204_NO_CONTENT)


# # author restore

# # NEWS


# class NewsArticleListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
#     queryset = NewsArticle.active_objects.all()
#     serializer_class = NewsArticleSerializer
#     renderer_classes = [CustomRenderer]


# class NewsArticleRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
#     queryset = NewsArticle.active_objects.all()
#     serializer_class = NewsArticleSerializer
#     renderer_classes = [CustomRenderer]
#     lookup_field = "pk"


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes((CustomRenderer,))
# def news_delete(request, pk):
#     news = NewsArticle.active_objects.get(pk=pk)
#     news.is_active = False
#     news.save()

#     return Response({"message": 'News was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


# # NEWSCOMMENT
# class NewsCommentListCreateAPIView(generics.ListCreateAPIView):
#     queryset = NewsComment.active_objects.all()[:10]
#     renderer_classes = [CustomRenderer, BrowsableAPIRenderer]
#     serializer_class = NewsCommentSerializer

#     def post(self, request, *args, **kwargs):
#         news_article = get_object_or_404(
#             NewsArticle, pk=self.kwargs.get('pk', None))
#         serializer = self.serializer_class(
#             data=request.data, context={'request': request})
#         print(serializer.is_valid())
#         if serializer.is_valid():
#             serializer.save(news_article=news_article)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NewsCommentRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
#     serializer_class = NewsCommentListCreateAPIView
#     queryset = NewsComment.active_objects.all()
#     renderer_classes = [CustomRenderer, ]

#     def get(self, request, *args, **kwargs):
#         newscomment = NewsComment.active_objects.get(
#             news_article__pk=self.kwargs.get('news_pk', None), pk=self.kwargs.get('pk', None))

#         serializer = self.serializer_class(newscomment)
#         if serializer.is_valid():
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes((CustomRenderer,))
# def newscomment_delete(request, news_pk, pk):
#     newscomment = NewsComment.active_objects.get(
#         news_article__pk=news_pk, pk=pk)
#     newscomment.is_active = False
#     newscomment.save()

#     return Response({"message": 'The Comment on the News was sucessfully deleted'}, status=status.HTTP_204_NO_CONTENT)


# # Gallery
# class GalleryListCreateAPIView(AdminOrReadOnlyMixin, generics.ListCreateAPIView):
#     queryset = Gallery.objects.all()
#     serializer_class = GallerySerializer


# class GalleryRetrieveUpdateAPIView(AdminOrReadOnlyMixin, generics.RetrieveUpdateAPIView):
#     queryset = Gallery.objects.all()
#     serializer_class = GallerySerializer
#     lookup_field = "pk"


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes([CustomRenderer, ])
# def gallery_delete(request, pk):
#     gallery = Gallery.objects.get(pk=pk)
#     gallery.is_active = False
#     gallery.save()

#     return Response({"message": 'The Image was sucessfully deleted'}, status=status.HTTP_204_NO_CONTENT)

# # Newsletter


# class NewsLetterSubscriptionListCreateAPIView(generics.ListCreateAPIView):
#     queryset = NewsLetterSubscription.objects.all()
#     serializer_class = NewsLetterSubscriptionSerializer
#     renderer_classes = [CustomRenderer, ]


# class NewsLetterSubscriptionRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
#     queryset = NewsLetterSubscription.objects.all()
#     serializer_class = NewsLetterSubscriptionSerializer
#     renderer_classes = [CustomRenderer, ]
#     lookup_field = "pk"


# @api_view(['DELETE'])
# @permission_classes([permissions.IsAdminUser])
# @renderer_classes([CustomRenderer, ])
# def newslettersubscription_delete(request, pk):
#     newsLetter = NewsLetterSubscription.objects.get(pk=pk)
#     newsLetter.is_active = False
#     newsLetter.save()

#     return Response({"message": 'The Subscription was sucessfully annulled'}, status=status.HTTP_204_NO_CONTENT)
