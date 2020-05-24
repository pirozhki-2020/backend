from django_serializer.v2.views import ListApiView, HttpMethod, GetApiView
from django_serializer.v2.views.paginator import FromIdPaginator, \
    DescFromIdPaginator

from alcohall.selections.models import Selection
from alcohall.selections.serializers import ListSelectionSerializer, SelectionSerializer


class SelectionsListView(ListApiView):
    class Meta:
        model = Selection
        tags = ['selections', ]
        method = HttpMethod.GET
        paginator = DescFromIdPaginator
        serializer = ListSelectionSerializer
        serializer_many = False

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-id')

    def build_response(self, qs, qs_after_paginator=None):
        return {'selections': qs_after_paginator}


class SelectionGetView(GetApiView):
    class Meta:
        model = Selection
        tags = ['selections', ]
        method = HttpMethod.GET
        serializer = SelectionSerializer
