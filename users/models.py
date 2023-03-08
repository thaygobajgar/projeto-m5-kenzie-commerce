from django.db import models
from django.contrib.auth.models import AbstractUser
from addresses.models import Address


class UserType(models.TextChoices):
    ADMINISTRADOR = 'Administrador'
    VENDEDOR = 'Vendedor'
    CLIENTE = 'Cliente'


class User(AbstractUser):
    user_type = models.CharField(
        max_length=50,
        choices=UserType.choices,
        default=UserType.CLIENTE,

    )
    username = models.CharField(
        max_length=127,
        unique=True,
        error_messages={"unique": "Username already exists"},
    )
    email = models.EmailField(
        max_length=127,
        unique=True,
        error_messages={"unique": "Email already registered"},
    )
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    address = Address