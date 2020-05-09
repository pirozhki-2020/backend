from django_serializer.v2.serializer import ModelSerializer, Serializer
from marshmallow import fields, pre_dump

from alcohall.cocktail.serializers import BaseCocktailSerializer
from alcohall.selections.models import Selection


class BaseSelectionSerializer(ModelSerializer):
    class SMeta:
        model = Selection


class SelectionSerializer(BaseSelectionSerializer):
    @pre_dump
    def prepare(self, obj: Selection, **kwargs):
        obj._cocktails = obj.cocktails.all()
        return obj

    cocktails = fields.Nested(BaseCocktailSerializer, many=True, attribute='_cocktails')


class ListSelectionSerializer(Serializer):
    selections = fields.Nested(BaseSelectionSerializer, many=True)
