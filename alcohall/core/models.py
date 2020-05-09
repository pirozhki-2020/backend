from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        if not username:
            raise User.DoesNotExist
        return super().get_by_natural_key(username)


class User(AbstractBaseUser):
    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    email = models.CharField('E-mail', max_length=30, unique=True, null=True)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email or f'{self.first_name} {self.last_name}'
