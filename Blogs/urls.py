from django.urls import path
from Blogs import views


app_name='Blogs'
urlpatterns = [
   path('blog-list/', views.BlogArticleListCreateAPIView.as_view(), name="article_list_create"),
   path('blog-detail/<int:pk>/', views.BlogArticleRetrieveUpdateAPIView.as_view(), name="article_detail_update"),
   path('blog-delete/<int:pk>/', views.article_delete, name='article_delete'),
   path('comment-list/', views.CommentListCreateAPIView.as_view(), name="comment_list_create"),
   path('comment-delete/<int:pk>/', views.comment_delete, name='comment_delete'),

   path('author-list/', views.AuthorListCreateAPIView.as_view(), name="author_list_create"),
   path('author-update/<int:pk>/', views.AuthorRetrieveUpdateAPIView.as_view(), name='author_update'),
   path('author-delete/<int:pk>/', views.author_delete, name='author_delete'),

   path('news-list/', views.NewsArticleListCreateAPIView.as_view(), name="news_list_create"),
   path('news-update/<int:pk>/', views.NewsArticleRetrieveUpdateAPIView.as_view(), name='news_update'),
   path('news-delete/<int:pk>/', views.news_delete, name='news_delete'),
   path('news-comment_list/', views.NewsCommentListCreateAPIView.as_view(), name="news_comment_list_create"),
   path('news-comment_delete/<int:pk>/', views.newscomment_delete, name='news_comment_delete'),

   path('gallery-list/', views.GalleryListCreateAPIView.as_view(), name="gallery_list_create"),
   path('gallery-update/<int:pk>/', views.GalleryRetrieveUpdateAPIView.as_view(), name='gallery_update'),
   path('gallery-delete/<int:pk>/', views.gallery_delete, name='gallery_delete'),

   path('newsletter-list/', views.NewsLetterSubscriptionListCreateAPIView.as_view(), name="gallery_list_create"),
   path('newsletter-update/<int:pk>/', views.NewsLetterSubscriptionRetrieveUpdateAPIView.as_view(), name='gallery_update'),
   path('newsletter-delete/<int:pk>/', views.newslettersubscription_delete, name='subscription_delete'),


]
