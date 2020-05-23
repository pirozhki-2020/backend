from django.urls import path

from alcohall.core import views

urlpatterns = [
    path('sign_up', views.SignUpView.as_view()),
    path('sign_in', views.SignInView.as_view()),
    path('get', views.GetView.as_view()),
]
