from django.contrib import admin
from django.contrib.admin import ModelAdmin

from alcohall.selections.models import Selection


@admin.register(Selection)
class SelectionAdmin(ModelAdmin):
    filter_horizontal = ("cocktails",)
