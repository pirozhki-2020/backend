# Generated by Django 3.0.4 on 2020-05-09 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cocktail", "0002_auto_20200509_1329"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="cocktail",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
                verbose_name="создатель",
            ),
        ),
        migrations.AddField(
            model_name="cocktail",
            name="image",
            field=models.ImageField(
                null=True, upload_to="", verbose_name="Изображение"
            ),
        ),
    ]
