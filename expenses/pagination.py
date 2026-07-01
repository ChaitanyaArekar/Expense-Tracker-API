from rest_framework.pagination import PageNumberPagination


class ExpensePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size" # allows clients to specify the number of items per page in the query parameters, e.g., ?page_size=20
    max_page_size = 100