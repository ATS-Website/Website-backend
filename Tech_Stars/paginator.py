from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class WebsitePaginator(PageNumberPagination):
    page_size = 10


# class CSVPaginator(PageNumberPagination):
#     page_size = 100

#     page_query_param = 'page'
#     max_page_size = 20

#     def get_paginated_response(self, data):
#         return Response({
#             "links": {
#                 "next": self.get_next_link(),
#                 "previous": self.get_previous_link()

#             },
#             "count": self.page.paginator.count,
#             "data": data,
#             "pageCount":  self.page.paginator.num_pages,
#             "pageNumber": self.page.number,
#             "pageSize":   self.page.paginator.per_page
#         })
