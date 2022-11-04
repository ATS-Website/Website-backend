from django.urls import path
from Blogs import views


# app_name = 'Blogs'
urlpatterns = [
    path('blogs', views.BlogArticleListCreateAPIView.as_view(),
         name="blog_list_create"),
    path('blogs/<int:pk>',
         views.BlogArticleRetrieveUpdateAPIView.as_view(), name="blog_detail_update"),
    path('blog-delete/<int:pk>', views.article_delete, name='article_delete'),
    path('<int:pk>/comments', views.CommentListCreateAPIView.as_view(),
         name="comment_list_create"),
    path('<int:blog_pk>/comment-delete/<int:pk>',
         views.comment_delete, name='comment_delete'),

    path('author', views.AuthorListCreateAPIView.as_view(),
         name="author_list_create"),
    path('author/<int:pk>',
         views.AuthorRetrieveUpdateAPIView.as_view(), name='author_detail_update'),
    path('author/<int:pk>', views.author_delete, name='author_delete'),

    path('news', views.NewsArticleListCreateAPIView.as_view(),
         name="news_list_create"),
    path('news/<int:pk>',
         views.NewsArticleRetrieveUpdateAPIView.as_view(), name='news_detail_update'),
    path('news/<int:pk>', views.news_delete, name='news_delete'),


    path('<int:pk>/comment', views.NewsCommentListCreateAPIView.as_view(),
         name="news_comment_list_create"),
    path('<int:news_pk>/comment/<int:pk>',
         views.newscomment_delete, name='news_comment_delete'),
    path('<int:news_pk>/comment/<int:pk>',
         views.NewsCommentRetrieveUpdateAPIView.as_view(), name='comment_detail_update'),

    path('gallery', views.GalleryListCreateAPIView.as_view(),
         name="gallery_list_create"),
    path('gallery/<int:pk>',
         views.GalleryRetrieveUpdateAPIView.as_view(), name='gallery_detail_update'),
    path('gallery/<int:pk>/', views.gallery_delete, name='gallery_delete'),

    path('newsletter-subscription-list-create/', views.NewsLetterSubscriptionListCreateAPIView.as_view(),
         name="newsletter_subscription_list_create"),
    path('newsletter-subscription-detail-update/<int:pk>/',
         views.NewsLetterSubscriptionRetrieveUpdateAPIView.as_view(), name='newsletter_subscription_detail_update'),
    path('newsletter-subscription-delete/<int:pk>/',
         views.newslettersubscription_delete, name='subscription_delete'),

    path('search-blog/', views.SearchBlogView.as_view(), name="search-blog"),
    path('search-news/', views.SearchNewsView.as_view(), name="search-news"),
]
