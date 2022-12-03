from rest_framework.pagination import PageNumberPagination


class WebsitePaginator(PageNumberPagination):
    page_size = 10


