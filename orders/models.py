from django.db import models
import uuid


class Status(models.TextChoices):
    ORDERED = "PEDIDO REALIZADO"
    IN_PROGRESS = "EM ANDAMENTO"
    DELIVERED = "ENTREGUE"


class Order(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ORDERED
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="orders"
    )
