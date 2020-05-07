from django.urls import path

from alcohall.cocktail import views

urlpatterns = [
    path('list_ingredients', views.ListIngredientView.as_view()),
    path('get_cocktail', views.GetCocktailView.as_view()),
    path('list_cocktails', views.ListCocktailView.as_view()),
    path('create', views.CreateCocktailView.as_view()),
]
