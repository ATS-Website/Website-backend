from django.urls import path
from Blogs import views


app_name='Blogs'
urlpatterns = [
   path('article_list/', views.BlogArticleListCreateAPIView.as_view(), name="article_list_create"),
   path('article_detail/<int:pk>/', views.BlogArticleRetrieveUpdateAPIView.as_view(), name="article_detail_update"),
   path('article_delete/<int:pk>/', views.article_delete, name='article_delete'),
   path('comment_list/', views.CommentListCreateAPIView.as_view(), name="comment_list_create"),
   path('comment_delete/<int:pk>/', views.comment_delete, name='comment_delete'),

   path('author_list/', views.AuthorListCreateAPIView.as_view(), name="author_list_create"),
   path('author_update/<int:pk>/', views.AuthorRetrieveUpdateAPIView.as_view(), name='author_update'),
   path('author_delete/<int:pk>/', views.author_delete, name='author_delete'),

   path('news_list/', views.NewsArticleListCreateAPIView.as_view(), name="news_list_create"),
   path('news_update/<int:pk>/', views.NewsArticleRetrieveUpdateAPIView.as_view(), name='news_update'),
   path('news_delete/<int:pk>/', views.news_delete, name='news_delete'),
   path('news_comment_list/', views.NewsCommentListCreateAPIView.as_view(), name="news_comment_list_create"),
   path('news_comment_delete/<int:pk>/', views.newscomment_delete, name='news_comment_delete'),

   path('gallery_list/', views.GalleryListCreateAPIView.as_view(), name="gallery_list_create"),
   path('gallery_update/<int:pk>/', views.GalleryRetrieveUpdateAPIView.as_view(), name='gallery_update'),
   path('gallery_delete/<int:pk>/', views.gallery_delete, name='gallery_delete'),

   path('newsletter_list/', views.NewsLetterSubscriptionListCreateAPIView.as_view(), name="gallery_list_create"),
   path('newsletter_update/<int:pk>/', views.NewsLetterSubscriptionRetrieveUpdateAPIView.as_view(), name='gallery_update'),
   path('newsletter_delete/<int:pk>/', views.newslettersubscription_delete, name='subscription_delete'),


]
