from django.contrib import admin
from django.contrib.admin import ModelAdmin

from alcohall.core.models import User, Like


@admin.register(User)
class UserAdmin(ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(ModelAdmin):
    pass
