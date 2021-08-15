from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Customized pagination class."""

    page_size_query_param = 'page_size'
