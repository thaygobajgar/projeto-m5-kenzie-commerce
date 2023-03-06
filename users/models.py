from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(
        max_length=127,
        unique=True,
        error_messages={"unique": "Email already registered"},
    )
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    is_employee = models.BooleanField(default=False)
