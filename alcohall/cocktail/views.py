import json

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django_serializer.v2.views.mixins import LoginRequiredMixin
from marshmallow.exceptions import ValidationError as marshmallowValidationError
from django_serializer.v2.exceptions import BadRequestError
from django_serializer.v2.views import HttpMethod, GetApiView, \
    ListApiView, ApiView

from alcohall.cocktail.models import Ingredient, Cocktail, CocktailIngredient, CocktailTool
from alcohall.cocktail.schemas import CreateCocktailSchema
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


class ListCocktailForm(forms.Form):
    ingredient = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all())


class ListCocktailView(ListApiView):
    class Meta:
        model = Cocktail
        method = HttpMethod.GET
        tags = ['cocktails', ]
        serializer = ListCocktailSerializer
        query_form = ListCocktailForm
        serializer_many = False

    def get_queryset(self):
        qs = super().get_queryset()
        ingredients = self.request_query['ingredient']

        qs = qs.filter(ingredients__in=ingredients) \
            .distinct() \
            .order_by('id')
        return {'cocktails': qs}


class CreateCocktailView(LoginRequiredMixin, ApiView):
    class Meta:
        model = Cocktail
        method = HttpMethod.POST
        serializer = CocktailSerializer
        tags = ['cocktails', ]

    def check_payload(self):
        try:
            payload = CreateCocktailSchema().load(json.loads(self.request.body))
        except marshmallowValidationError as e:
            raise BadRequestError(description=e.messages)
        return payload

    def execute(self, request, *args, **kwargs):
        payload = self.check_payload()

        with transaction.atomic():
            cocktail = Cocktail.objects.create(name=payload['name'], description=payload['description'],
                                               image_link=payload['image_link'], steps=payload['steps'],
                                               author=self.request.user)
            for ingredient_id, volume in payload['ingredients'].items():
                CocktailIngredient.objects.create(cocktail=cocktail, ingredient_id=ingredient_id, volume=volume)
            for tool_id, number in payload['tools'].items():
                CocktailTool.objects.create(cocktail=cocktail, tool_id=tool_id, number=number)

        return cocktail
