from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Like(models.Model):
    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    cocktail = models.ForeignKey(
        "cocktail.Cocktail", on_delete=models.CASCADE, verbose_name="Коктейль"
    )
    is_active = models.BooleanField(default=False, verbose_name="Активный?")

    def __str__(self):
        return f"{self.user.email} {self.cocktail.name}"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email) or None
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        if not username:
            raise User.DoesNotExist
        return super().get_by_natural_key(username)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    first_name = models.CharField("Имя", max_length=30)
    last_name = models.CharField("Фамилия", max_length=30)
    email = models.CharField("E-mail", max_length=30, unique=True, null=True)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    is_superuser = models.BooleanField(default=False, verbose_name="Администратор")

    likes = models.ManyToManyField(
        "cocktail.Cocktail", through=Like, verbose_name="Лайки пользователя"
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email or f"{self.first_name} {self.last_name}"
