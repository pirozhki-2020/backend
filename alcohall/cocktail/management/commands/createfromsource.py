import json

from django.core.management.base import BaseCommand

from alcohall.cocktail.models import Cocktail, Ingredient, Tool, CocktailTool, \
    CocktailIngredient


class Command(BaseCommand):
    help = 'Creates cocktail models from json source'
    cocktail_tools = set()
    cocktail_ingredients = set()

    def add_arguments(self, parser):
        parser.add_argument('--file', '-f', default='data/sources.json',
                            help='path to source json file')
        parser.add_argument('--number', '-n', default=None,
                            help='number of models to create')

    def handle(self, *args, **options):
        try:
            f = open(options['file'], 'r')
        except FileNotFoundError:
            self.stderr.write(f'File {options["file"]} is not found')
            return

        cocktails = json.load(f)['cocktails']
        number = 0
        cocktails_number = len(cocktails)
        for cocktail in cocktails:
            if number % 50 == 0:
                print(f'{number} from {cocktails_number} prepared')
            cocktail_model = Cocktail.objects.create(
                name=cocktail['name'],
                description=cocktail['description'],
                image_link=cocktail['image_link'],
                steps=cocktail['recipe_steps'])
            for i, item in enumerate(cocktail['ingredients']):
                ingredient, _ = Ingredient.objects.get_or_create(name=item)
                CocktailIngredient.objects.create(
                    cocktail=cocktail_model,
                    ingredient=ingredient,
                    volume=cocktail['ingredients_amounts'][i])
            for i, item in enumerate(cocktail['tools']):
                tool, _ = Tool.objects.get_or_create(name=item)
                CocktailTool.objects.create(
                    cocktail=cocktail_model,
                    tool=tool,
                    number=cocktail['tools_amounts'][i])
            number += 1
        f.close()
