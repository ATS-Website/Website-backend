from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class ResponsePagination(PageNumberPagination):
    page_size = 2
    # page_query_params = 'p'
    # page_size_query_param = 'size'
    # max_page_size = 2
    # last_page_strings = 'end'

    # def get_paginated_response(self, data):
    #     return Response({
    #         "links": {
    #             "next": self.get_next_link(),
    #             "previous": self.get_previous_link()

    #         },
    #         "count": self.page.paginator.count,
    #         "results": data
    #     })
