from django.urls import path
from Blogs.views import (AuthorListCreateAPIView, AuthorRetrieveUpdateAPIView,
                         TagListCreateAPIView, TagDetailUpdateDeleteAPIView,
                         BlogArticleListCreateAPIView, BlogArticleRetrieveUpdateDeleteAPIView,
                         CommentListCreateAPIView, CommentDetailsUpdateDeleteAPIView,
                         NewsArticleListCreateAPIView, NewsArticleRetrieveUpdateDeleteAPIView,
                         CategoryListCreateAPIView, CategoryDetailUpdateDeleteAPIView,
                         NewsLetterSubscriptionRetrieveUpdateDeleteAPIView, NewsLetterSubscriptionListCreateAPIView,
                         SendNewsLetter, NewsLetterListCreateAPIView, NewsLetterDetailsUpdateDeleteAPIView,
                         SearchNewsView, SearchBlogView, BlogArticleCommentListAPIView,
                         ViewsListCreateAPIView
                         )

app_name = 'Blogs'

urlpatterns = [
    path('blogs', BlogArticleListCreateAPIView.as_view(), name="blog_list_create"),
    path('blogs/<int:pk>', BlogArticleRetrieveUpdateDeleteAPIView.as_view(), name="blog_detail_update"),
    path("blogs-comments/<int:pk>", BlogArticleCommentListAPIView.as_view(), name="blog_comments"),

    path('comment', CommentListCreateAPIView.as_view(), name="comment_list_create"),
    path('comment/<int:pk>', CommentDetailsUpdateDeleteAPIView.as_view(), name='comment_detail_update_delete'),

    path('tag', TagListCreateAPIView.as_view(), name='tag-list'),
    path("tag/<int:pk>", TagDetailUpdateDeleteAPIView.as_view(), name="tag_detail_update_delete"),

    path('author', AuthorListCreateAPIView.as_view(),
         name="author_list_create"),
    path('author/<int:pk>',
         AuthorRetrieveUpdateAPIView.as_view(), name='author_detail_update'),

    path("category", CategoryListCreateAPIView.as_view(), name="category_list_create"),
    path("category/<int:pk>", CategoryDetailUpdateDeleteAPIView.as_view(), name="category_detail_update_delete"),

    path('news', NewsArticleListCreateAPIView.as_view(),
         name="news_list_create"),
    path('news/<int:pk>',
         NewsArticleRetrieveUpdateDeleteAPIView.as_view(), name='news_detail_update'),

    path("views", ViewsListCreateAPIView.as_view(), name="views_list_create"),

    #
    # path('gallery', views.GalleryListCreateAPIView.as_view(),
    #      name="gallery_list_create"),
    # path('gallery/<int:pk>',
    #      views.GalleryRetrieveUpdateAPIView.as_view(), name='gallery_detail_update'),
    # path('gallery/<int:pk>/', views.gallery_delete, name='gallery_delete'),
    #
    # path('gallery-list-create/', views.GalleryListCreateAPIView.as_view(), name="gallery_list_create"),
    # path('gallery-detail-update/<int:pk>/', views.GalleryRetrieveUpdateAPIView.as_view(),
    # name='gallery_detail_update'), path('gallery-delete/<int:pk>/', views.gallery_delete, name='gallery_delete'),
    #

    path("newsletter", NewsLetterListCreateAPIView.as_view(), name="newsletter_list_create"),
    path("newsletter/<int:pk>", NewsLetterDetailsUpdateDeleteAPIView.as_view(),
         name="newsletter_details_update_delete"),

    path('newsletter-subscription-list-create', NewsLetterSubscriptionListCreateAPIView.as_view(),
         name="newsletter_subscription_list_create"),
    path('newsletter-subscription-detail-update/<int:pk>', NewsLetterSubscriptionRetrieveUpdateDeleteAPIView.as_view(),
         name='newsletter_subscription_detail_update'),

    path("send-newsletter/<int:pk>", SendNewsLetter.as_view(), name="send_newsletter"),

    path('search-blog/', SearchBlogView.as_view(), name="search-blog"),
    path('search-news/', SearchNewsView.as_view(), name="search-news"),
]
