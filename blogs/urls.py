from django.urls import path
from blogs import views
from rest_framework import routers

from blogs.views import (AuthorListCreateAPIView, AuthorRetrieveUpdateAPIView,
                         BlogArticleListCreateAPIView, BlogArticleRetrieveUpdateDeleteAPIView,
                         CommentListCreateAPIView, CommentDetailsUpdateDeleteAPIView,
                         NewsArticleListCreateAPIView, NewsArticleRetrieveUpdateDeleteAPIView,
                         CategoryListCreateAPIView, CategoryDetailUpdateDeleteAPIView,
                         NewsLetterSubscriptionRetrieveUpdateDeleteAPIView, NewsLetterSubscriptionListCreateAPIView,
                         SendNewsLetter, NewsLetterListCreateAPIView, NewsLetterDetailsUpdateDeleteAPIView,
                         SearchNewsView, SearchBlogView, BlogArticleCommentListAPIView,
                         ViewsListCreateAPIView, LikesCreateAPIView, CategoryNewsCountAPIView, ImageListAPIView,
                         AlbumListCreateAPIView, AlbumRetrieveUpdateDeleteAPIView, NavNewsListAPIView, TrashedBlogListAPIView,
                         TrashedBlogRestoreAPIView, TrashedNewsListAPIView, TrashedNewsRestoreAPIView, TrashedAuthorListAPIView,
                         TrashedAuthorRestoreAPIView, TrashedCommentListAPIView, TrashedCommentRestoreAPIView, TrashedImageListAPIView,
                         TrashedImageRestoreAPIView, VisitorListCreateView, UpdatesNumbersListView
                         )

app_name = 'blogs'

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'news-search', views.NewsArticleDocumentView,
                basename='article-search')
router.register(r'blog-search', views.NewsArticleDocumentView,
                basename='article-search')
# router.register(r'news-search', views.global_search,
#                 basename='article-search')

urlpatterns = [
    path('blogs', BlogArticleListCreateAPIView.as_view(), name="blog_list_create"),
    path('blogs/<int:pk>', BlogArticleRetrieveUpdateDeleteAPIView.as_view(),
         name="blog_detail_update"),
    path('trash-blog', TrashedBlogListAPIView.as_view(), name="trash_blog_list"),
    path('trash-blog-restore/<int:pk>',
         TrashedBlogRestoreAPIView.as_view(), name='trash_blog_restore'),
    path("blogs-comments/<int:pk>",
         BlogArticleCommentListAPIView.as_view(), name="blog_comments"),

    path('comment', CommentListCreateAPIView.as_view(),
         name="comment_list_create"),
    path('comment/<int:pk>', CommentDetailsUpdateDeleteAPIView.as_view(),
         name='comment_detail_update_delete'),
    path('trash-comment', TrashedCommentListAPIView.as_view(), name='trash_comment'),
    path('trash-comment-restore/<int:pk>',
         TrashedCommentRestoreAPIView.as_view(), name='trash_comment_restore'),


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
    path('trash-author', TrashedAuthorListAPIView.as_view(), name='trash_author'),
    path('trash-author-restore/<int:pk>',
         TrashedAuthorRestoreAPIView.as_view(), name='trash_author_restore'),

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
    path('trash-news',  TrashedNewsListAPIView.as_view(), name='tash_news'),
    path('trash-news-restore/<int:pk>',
         TrashedNewsRestoreAPIView.as_view(), name='trash_news_restore'),

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
    path("images-trash", TrashedImageListAPIView.as_view(), name="images_trash"),
    path("images-trash-restore/<int:pk>",
         TrashedImageRestoreAPIView.as_view(), name="images_trash-restore"),

    path("album", AlbumListCreateAPIView.as_view(), name="album_list_create"),
    path("album/<int:pk>", AlbumRetrieveUpdateDeleteAPIView.as_view(),
         name="album_retrieve_update_delete"),

    path("nav-news", NavNewsListAPIView.as_view(), name="nav_news_list"),

    path("visitors", VisitorListCreateView.as_view(), name="visitors_list_create"),

    path("updates", UpdatesNumbersListView.as_view(), name="update_numbers"),





    path('search-blog/', SearchBlogView.as_view(), name="search-blog"),
    path('search-news/', SearchNewsView.as_view(), name="search-news"),
]
urlpatterns += router.urls
