from django.urls import path
from alcohall.ingredients.views import *

urlpatterns = [
    path('list_sizes', ListSizeView.as_view()),
]
