from django.urls import path
from Blogs import views
from rest_framework import routers

from Blogs.views import (AuthorListCreateAPIView, AuthorRetrieveUpdateAPIView,
                         BlogArticleListCreateAPIView, BlogArticleRetrieveUpdateDeleteAPIView,
                         CommentListCreateAPIView, CommentDetailsUpdateDeleteAPIView,
                         NewsArticleListCreateAPIView, NewsArticleRetrieveUpdateDeleteAPIView,
                         CategoryListCreateAPIView, CategoryDetailUpdateDeleteAPIView,
                         NewsLetterSubscriptionRetrieveUpdateDeleteAPIView, NewsLetterSubscriptionListCreateAPIView,
                         SendNewsLetter, NewsLetterListCreateAPIView, NewsLetterDetailsUpdateDeleteAPIView,
                         SearchNewsView, SearchBlogView, BlogArticleCommentListAPIView,
                         ViewsListCreateAPIView, LikesCreateAPIView, CategoryNewsCountAPIView, ImageListAPIView,
                         AlbumListCreateAPIView, AlbumRetrieveUpdateDeleteAPIView, NavNewsListAPIView
                         )

app_name = 'Blogs'

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'news-search', views.NewsArticleDocumentView,
                basename='article-search')
router.register(r'blog-search', views.NewsArticleDocumentView,
                basename='article-search')

urlpatterns = [
    path('blogs', BlogArticleListCreateAPIView.as_view(), name="blog_list_create"),
    path('blogs/<int:pk>', BlogArticleRetrieveUpdateDeleteAPIView.as_view(),
         name="blog_detail_update"),
    path("blogs-comments/<int:pk>",
         BlogArticleCommentListAPIView.as_view(), name="blog_comments"),

    path('comment', CommentListCreateAPIView.as_view(),
         name="comment_list_create"),
    path('comment/<int:pk>', CommentDetailsUpdateDeleteAPIView.as_view(),
         name='comment_detail_update_delete'),

    #     path('tag', TagListCreateAPIView.as_view(), name='tag-list'),
    #     path("tag/<int:pk>", TagDetailUpdateDeleteAPIView.as_view(),
    #          name="tag_detail_update_delete"),
    #     path('blogs/<int:pk>', BlogArticleRetrieveUpdateDeleteAPIView.as_view(), name="blog_detail_update"),
    #     path("blogs-comments/<int:pk>", BlogArticleCommentListAPIView.as_view(), name="blog_comments"),

    #     path('comment', CommentListCreateAPIView.as_view(), name="comment_list_create"),
    #     path('comment/<int:pk>', CommentDetailsUpdateDeleteAPIView.as_view(), name='comment_detail_update_delete'),

    path('author', AuthorListCreateAPIView.as_view(),
         name="author_list_create"),
    path('author/<int:pk>',
         AuthorRetrieveUpdateAPIView.as_view(), name='author_detail_update'),

    path("category", CategoryListCreateAPIView.as_view(),
         name="category_list_create"),
    path("category/<int:pk>", CategoryDetailUpdateDeleteAPIView.as_view(),
         name="category_detail_update_delete"),
    path("category-news-count", CategoryNewsCountAPIView.as_view(),
         name="category_news_count"),

    path('news', NewsArticleListCreateAPIView.as_view(),
         name="news_list_create"),
    path('news/<int:pk>',
         NewsArticleRetrieveUpdateDeleteAPIView.as_view(), name='news_detail_update'),

    path("views", ViewsListCreateAPIView.as_view(), name="views_list_create"),
    path("likes", LikesCreateAPIView.as_view(), name="likes_list_create"),

    #

    path("newsletter", NewsLetterListCreateAPIView.as_view(),
         name="newsletter_list_create"),
    path("newsletter/<int:pk>", NewsLetterDetailsUpdateDeleteAPIView.as_view(),
         name="newsletter_details_update_delete"),

    path('newsletter-subscription-list-create', NewsLetterSubscriptionListCreateAPIView.as_view(),
         name="newsletter_subscription_list_create"),
    path('newsletter-subscription-detail-update/<int:pk>', NewsLetterSubscriptionRetrieveUpdateDeleteAPIView.as_view(),
         name='newsletter_subscription_detail_update'),

    path("send-newsletter/<int:pk>",
         SendNewsLetter.as_view(), name="send_newsletter"),

    path("images", ImageListAPIView.as_view(), name="images_list"),

    path("album", AlbumListCreateAPIView.as_view(), name="album_list_create"),
    path("album/<int:pk>", AlbumRetrieveUpdateDeleteAPIView.as_view(), name="album_retrieve_update_delete"),

    path("nav-news", NavNewsListAPIView.as_view(), name="nav_news_list"),



    path('search-blog/', SearchBlogView.as_view(), name="search-blog"),
    path('search-news/', SearchNewsView.as_view(), name="search-news"),

]
urlpatterns += router.urls
