from rest_framework.pagination import PageNumberPagination


class SizeQueryPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "size"
    max_page_size = 100
