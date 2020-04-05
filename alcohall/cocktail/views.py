from django import forms
from django.core.exceptions import ValidationError
from django_serializer.v2.views import ApiView, HttpMethod, GetApiView

from alcohall.cocktail.models import Ingredient, Cocktail
from alcohall.cocktail.serializers import IngredientListSerializer, \
    CocktailSerializer


class ListIngredientForm(forms.Form):
    query = forms.CharField(required=False)
    id = forms.ModelMultipleChoiceField(
        required=False, queryset=Ingredient.objects.all())

    def clean(self):
        query = self.cleaned_data.get('query', None)
        ingredients = self.cleaned_data.get('id', None)
        if query is None and ingredients is None:
            raise ValidationError(
                {'__all__': 'at least one parameter: "query" or "id" should '
                            'be define'})
        return self.cleaned_data


class ListIngredientView(ApiView):
    class Meta:
        model = Ingredient
        method = HttpMethod.GET
        tags = ['ingredients', ]
        serializer = IngredientListSerializer
        query_form = ListIngredientForm

    def execute(self, request, *args, **kwargs):
        if self.request_query['id']:
            return {'ingredients': self.request_query['id']}

        qs = Ingredient.objects.filter(
            name__istartswith=self.request_query['query'])
        return {'ingredients': qs.all()}


class GetCocktailView(GetApiView):
    class Meta:
        model = Cocktail
        method = HttpMethod.GET
        tags = ['cocktails', ]
        serializer = CocktailSerializer
