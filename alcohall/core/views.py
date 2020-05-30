from django import forms
from django.contrib.auth import authenticate, login, logout
from django_serializer.v2.exceptions import AuthRequiredError
from django_serializer.v2.views import HttpMethod, ApiView, ListApiView
from django_serializer.v2.views.mixins import LoginRequiredMixin

from alcohall.cocktail.models import Cocktail
from alcohall.cocktail.serializers import ListCocktailSerializer
from alcohall.core.errors import EmailAlreadyRegistered
from alcohall.core.models import User
from alcohall.core.serializers import UserSerializer


class CredentialsForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class SignUpView(ApiView):
    class Meta:
        tags = [
            "user",
        ]
        method = HttpMethod.POST
        body_form = CredentialsForm
        serializer = UserSerializer

    def execute(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return self.request.user

        email, password = self.request_body["email"], self.request_body["password"]
        existed_user = User.objects.filter(email=email)
        if existed_user.exists():
            raise EmailAlreadyRegistered
        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()

        login(request, user)
        return user


class SignInView(ApiView):
    class Meta:
        tags = [
            "user",
        ]
        method = HttpMethod.POST
        body_form = CredentialsForm
        serializer = UserSerializer

    def execute(self, request, *args, **kwargs):
        email, password = self.request_body["email"], self.request_body["password"]
        user = authenticate(request, username=email, password=password)
        if not user:
            raise AuthRequiredError
        login(request, user)
        return user


class LogoutView(LoginRequiredMixin, ApiView):
    class Meta:
        tags = [
            "user",
        ]
        method = HttpMethod.POST

    def execute(self, request, *args, **kwargs):
        logout(request)
        return {}


class GetView(LoginRequiredMixin, ApiView):
    class Meta:
        tags = [
            "user",
        ]
        method = HttpMethod.GET
        serializer = UserSerializer

    def execute(self, request, *args, **kwargs):
        return self.request.user


class LikedView(LoginRequiredMixin, ListApiView):
    class Meta:
        model = Cocktail
        tags = [
            "user",
        ]
        method = HttpMethod.GET
        serializer = ListCocktailSerializer
        serializer_many = False

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs.filter(like__user=self.request.user, like__is_active=True)
            .distinct()
            .order_by("id")
        )
        return {"cocktails": qs}
