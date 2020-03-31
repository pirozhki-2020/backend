from django.contrib import admin

from alcohall.ingredients.models import Size


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size',)
    exclude = ('order',)
