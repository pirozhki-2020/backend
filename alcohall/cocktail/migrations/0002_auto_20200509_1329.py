# Generated by Django 3.0.4 on 2020-05-09 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktail', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cocktail',
            old_name='image_link',
            new_name='source_image_link',
        ),
    ]