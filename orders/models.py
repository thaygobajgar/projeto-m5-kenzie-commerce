from django.db import models


class Status(models.TextChoices):
    ORDERED = "PEDIDO REALIZADO"
    IN_PROGRESS = "EM ANDAMENTO"
    DELIVERED = "ENTREGUE"


class Order(models.Model):
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ORDERED
    )
    users = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="orders"
    )
