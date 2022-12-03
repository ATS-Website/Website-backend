from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class WebsitePaginator(PageNumberPagination):
    page_size = 10


