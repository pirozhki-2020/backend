from django.db import models


class Size(models.Model):
    class Meta:
        verbose_name = 'объем'
        verbose_name_plural = 'объемы'
        ordering = ['size']

    size = models.PositiveIntegerField(verbose_name='объем')

    def __str__(self):
        return f'{self.size} мл.'


class Ingredient(models.Model):
    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    name = models.CharField(max_length=64, verbose_name='название')

    def __str__(self):
        return f'{self.name}'
