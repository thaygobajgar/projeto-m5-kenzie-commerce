from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=127)
    number = models.IntegerField()
    city = models.CharField(max_length=127)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=8)

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="address"
    )
