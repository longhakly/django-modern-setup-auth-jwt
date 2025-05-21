from os import environ

# Default to using local django if the DJANGO_ENV variable is not set
DJANGO_ENV = environ.get("DJANGO_ENV", "local")

if DJANGO_ENV == "prod":
    from .django.prod import *
elif DJANGO_ENV == "local":
    from .django.local import *
else:
    from .django.base import *
