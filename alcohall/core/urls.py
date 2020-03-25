from django.urls import path

from alcohall.core import views

urlpatterns = [
    path('', views.index)
]