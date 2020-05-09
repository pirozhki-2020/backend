from django.contrib.auth.models import User
from django_serializer.v2.serializer import ModelSerializer


class UserSerializer(ModelSerializer):
    class SMeta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'password', 'last_login', 'is_active',)
