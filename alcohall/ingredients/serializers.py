from django_serializer.v2.serializer import ModelSerializer

from alcohall.ingredients.models import Size


class SizeSerializer(ModelSerializer):
    class SMeta:
        model = Size
