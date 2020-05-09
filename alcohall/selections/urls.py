from django.urls import path

from alcohall.selections import views

urlpatterns = [
    path('list', views.SelectionsListView.as_view()),
    path('get', views.SelectionGetView.as_view()),
]
