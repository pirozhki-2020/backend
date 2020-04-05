from django_serializer.v2.serializer import ModelSerializer, Serializer
from marshmallow import fields, pre_dump, post_dump

from alcohall.cocktail.models import Ingredient, Cocktail, Tool, \
    CocktailIngredient, CocktailTool


class IngredientSerializer(ModelSerializer):
    class SMeta:
        model = Ingredient


class ToolSerializer(ModelSerializer):
    class SMeta:
        model = Tool


class CocktailToolSerializer(ModelSerializer):
    class SMeta:
        model = CocktailTool
        exclude = ('cocktail_id', 'tool_id', 'id',)

    @post_dump
    def prepare(self, data: dict, **kwargs):
        data['id'] = data['tool']['id']
        data['name'] = data['tool']['name']
        data.pop('tool')
        return data

    tool = fields.Nested(ToolSerializer)


class CocktailIngredientSerializer(ModelSerializer):
    class SMeta:
        model = CocktailIngredient
        exclude = ('cocktail_id', 'ingredient_id', 'id',)

    @post_dump
    def prepare(self, data: dict, **kwargs):
        data['id'] = data['ingredient']['id']
        data['name'] = data['ingredient']['name']
        data.pop('ingredient')
        return data

    ingredient = fields.Nested(IngredientSerializer)


class IngredientListSerializer(Serializer):
    ingredients = fields.Nested(IngredientSerializer, many=True)


class CocktailSerializer(ModelSerializer):
    class SMeta:
        model = Cocktail

    @pre_dump
    def prepare(self, obj: Cocktail, **kwargs):
        obj._ingredients = obj.cocktailingredient_set.all()
        obj._tools = obj.cocktailtool_set.all()
        return obj

    ingredients = fields.Nested(CocktailIngredientSerializer, many=True,
                                attribute='_ingredients')
    tools = fields.Nested(CocktailToolSerializer, many=True, attribute='_tools')
