from django_serializer.v2.exceptions import HttpError


class EmailAlreadyRegistered(HttpError):
    def __init__(self):
        super().__init__(
            http_code=409,
            alias='already_registered',
            description='The email is already registered'
        )