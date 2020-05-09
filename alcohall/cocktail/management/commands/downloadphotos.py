import os

import requests
from django.core.management.base import BaseCommand

from alcohall.application.settings import MEDIA_ROOT
from alcohall.cocktail.models import Cocktail

MIME_TO_EXTENSION_MAP = {
    'image/jpeg': 'jpeg',
    'image/gif': 'gif',
    'image/png': 'png'
}

BASE_URL = 'https://ru.inshaker.com'


class Command(BaseCommand):
    help = 'Creates cocktail models from json source'
    cocktail_tools = set()
    cocktail_ingredients = set()

    def handle(self, *args, **options):
        cocktails = Cocktail.objects.filter(image=None)
        progress, total = 0, cocktails.count()
        self.stdout.write(f'{total} cocktails need image')

        for cocktail in cocktails:
            if progress % 10 == 0:
                self.stdout.write(f'{progress}/{total}')
            progress += 1
            url = BASE_URL + cocktail.source_image_link
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                extension = MIME_TO_EXTENSION_MAP[response.headers.get('Content-Type')]
                filename = f'{cocktail.name}_{cocktail.id}_image.{extension}'
                with open(os.path.join(MEDIA_ROOT, filename), 'wb') as f:
                    f.write(response.content)
                cocktail.image.name = filename
                cocktail.save(update_fields=['image'])
            else:
                self.stderr.write(f'can not load image. source_image_link: {cocktail.source_image_link}, '
                                  f'status_code: {response.status_code}')
