from django_serializer.v2.views import ListApiView, HttpMethod

from alcohall.ingredients.models import Size
from alcohall.ingredients.serializers import SizeSerializer


class ListSizeView(ListApiView):
    class Meta:
        model = Size
        tags = ['ingredients', ]
        method = HttpMethod.GET
        serializer = SizeSerializer
