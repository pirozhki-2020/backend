ALLOWED_HOSTS = ["alcohall.space", "www.alcohall.space"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "alcohall-db",
        "PORT": 5432,
    }
}

STATIC_ROOT = "/static"
MEDIA_ROOT = "/media"
