from marshmallow import Schema, fields


class CreateCocktailSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    steps = fields.List(fields.String, required=True)
    ingredients = fields.Dict(fields.Int, fields.Float, required=True)
    tools = fields.Dict(fields.Int, fields.Float, required=True)
    image_link = fields.URL(required=True)
