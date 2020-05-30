from django import forms
from django_serializer.v2.views import ListApiView, HttpMethod, GetApiView, ApiView
from django_serializer.v2.views.paginator import DescFromIdPaginator

from alcohall.cocktail.models import Cocktail
from alcohall.selections.models import Selection
from alcohall.selections.serializers import ListSelectionSerializer, SelectionSerializer


class SelectionsListView(ListApiView):
    class Meta:
        model = Selection
        tags = [
            "selections",
        ]
        method = HttpMethod.GET
        paginator = DescFromIdPaginator
        serializer = ListSelectionSerializer
        serializer_many = False

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by("-id")

    def build_response(self, qs, qs_after_paginator=None):
        return {"selections": qs_after_paginator}


class SelectionGetView(GetApiView):
    class Meta:
        model = Selection
        tags = [
            "selections",
        ]
        method = HttpMethod.GET
        serializer = SelectionSerializer


class SelectionCreateForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    cocktails = forms.ModelMultipleChoiceField(
        queryset=Cocktail.objects.all(), required=True
    )


class SelectionCreateView(ApiView):
    class Meta:
        tags = [
            "selections",
        ]
        method = HttpMethod.POST
        serializer = SelectionSerializer
        body_form = SelectionCreateForm

    def execute(self, request, *args, **kwargs):
        selection = Selection.objects.create(
            name=self.request_body["name"], description=self.request_body["description"]
        )
        cocktails = self.request_body["cocktails"]
        selection.cocktails.add(*cocktails)
        return selection
