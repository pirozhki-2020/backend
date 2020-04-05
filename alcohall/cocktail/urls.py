from django.urls import path

from alcohall.cocktail import views

urlpatterns = [
    path('get_ingredient', views.ListIngredientView.as_view()),
    path('get_cocktail', views.GetCocktailView.as_view()),
]
