from django.db import models


class List(models.Model):
    name = models.CharField(max_length=127)

    products = models.ManyToManyField(
        "products.Product",
        related_name="lists",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="lists",
    )
