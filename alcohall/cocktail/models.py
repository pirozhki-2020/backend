from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField
from alcohall.core.models import User


class Ingredient(models.Model):
    class Meta:
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"

    name = models.CharField(max_length=128, verbose_name="название")

    def __str__(self):
        return self.name


class Tool(models.Model):
    class Meta:
        verbose_name = "инструмент"
        verbose_name_plural = "инструмент"

    name = models.CharField(max_length=128, verbose_name="название")

    def __str__(self):
        return self.name


class Cocktail(models.Model):
    class Meta:
        verbose_name = "коктейль"
        verbose_name_plural = "коктейли"

    name = models.CharField(max_length=128, verbose_name="название")
    description = models.CharField(max_length=512, verbose_name="описание")
    ingredients = models.ManyToManyField(
        Ingredient, through="CocktailIngredient", verbose_name="ингредиенты"
    )
    tools = models.ManyToManyField(
        Tool, through="CocktailTool", verbose_name="инструменты"
    )
    steps = ArrayField(models.CharField(max_length=512), verbose_name="шаги рецепта")
    source_image_link = models.CharField(
        max_length=128, verbose_name="ссылка на фотографию"
    )
    image = models.ImageField(verbose_name="Изображение", null=True)
    author = models.ForeignKey(
        User, null=True, on_delete=models.DO_NOTHING, verbose_name="создатель"
    )

    @property
    def image_link(self):
        return self.image.url

    def __str__(self):
        return self.name


class CocktailIngredient(models.Model):
    cocktail = models.ForeignKey(
        Cocktail, on_delete=models.CASCADE, verbose_name="коктейль"
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name="ингредиент"
    )
    volume = models.FloatField(verbose_name="объем")


class CocktailTool(models.Model):
    cocktail = models.ForeignKey(
        Cocktail, on_delete=models.CASCADE, verbose_name="коктейль"
    )
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, verbose_name="инструмент")
    number = models.IntegerField()
