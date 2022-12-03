from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10

    """Custom page number pagination."""

    def get_paginated_response_context(self, data):

        __data = super(CustomPageNumberPagination,
                       self).get_paginated_response_context(data)
        __data.append(
            ('current_page', int(self.request.query_params.get('page', 10)))
        )
        __data.append(
            ('page_size', self.get_page_size(self.request))
        )
        return sorted(__data)


class ResponsePagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10

