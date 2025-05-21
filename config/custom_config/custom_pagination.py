from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    def get_page_size(self, request):
        page_size = request.query_params.get("page_size", 10)
        try:
            return int(page_size)
        except (ValueError, TypeError):
            return self.page_size

    def paginate_queryset(self, queryset, request, view=None):
        paging = request.query_params.get("paging", "true")

        if paging not in ["true", "True"]:
            return None

        self.page_size = self.get_page_size(request)
        self.request = request
        self.queryset = queryset

        return super().paginate_queryset(queryset, request, view) 

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "page_size": self.page_size,
                "results": data,
            }
        )
