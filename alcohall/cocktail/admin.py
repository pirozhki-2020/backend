from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from alcohall.cocktail.models import Cocktail, Ingredient, Tool, \
    CocktailIngredient, CocktailTool


class CocktailIngredientAdmin(admin.StackedInline):
    model = CocktailIngredient
    extra = 0


class CocktailToolAdmin(admin.StackedInline):
    model = CocktailTool
    extra = 0


@admin.register(Cocktail)
class CocktailAdmin(admin.ModelAdmin, DynamicArrayMixin):
    inlines = (CocktailIngredientAdmin, CocktailToolAdmin)
    list_display = ('id', 'name',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)
    search_fields = ('name',)
