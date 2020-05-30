from django.db import models

from alcohall.cocktail.models import Cocktail


class Selection(models.Model):
    class Meta:
        verbose_name = "подборка"
        verbose_name_plural = "подборки"

    name = models.CharField(max_length=32, verbose_name="Название")
    description = models.CharField(max_length=512, verbose_name="Описание")
    cocktails = models.ManyToManyField(Cocktail)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name
