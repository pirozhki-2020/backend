from django import forms
from django.core.exceptions import ValidationError
from django_serializer.v2.exceptions import BadRequestError
from django_serializer.v2.views import HttpMethod, GetApiView, \
    ListApiView

from alcohall.cocktail.models import Ingredient, Cocktail
from alcohall.cocktail.serializers import ListIngredientSerializer, \
    CocktailSerializer, ListCocktailSerializer


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


class ListIngredientView(ListApiView):
    class Meta:
        model = Ingredient
        method = HttpMethod.GET
        tags = ['ingredients', ]
        serializer = ListIngredientSerializer
        serializer_many = False
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


class ListCocktailView(ListApiView):
    class Meta:
        model = Cocktail
        method = HttpMethod.POST
        tags = ['cocktails', ]
        serializer = ListCocktailSerializer
        serializer_many = False

    def check_payload(self):
        self.get_request_json()
        payload = getattr(self, '_request_json', None)
        if not payload:
            raise BadRequestError('empty body')
        ingredients = payload.get('ingredients', None)
        if not ingredients:
            raise BadRequestError('missing or invalid ingredients field')
        ingredients_ids = set()
        for ingredient in ingredients:
            if not ingredient.get('id') or not ingredient.get('volume'):
                raise BadRequestError('wrong ingredient format')
            ingredients_ids.add(ingredient.get('id'))
        payload['ingredients_ids'] = ingredients_ids
        return payload

    def get_queryset(self):
        payload = self.check_payload()
        qs = super().get_queryset()
        qs = qs.filter(
            cocktailingredient__in=payload['ingredients_ids']) \
            .distinct() \
            .order_by('id')
        return {'cocktails': qs}
