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
        max_length=16,
        choices=Status.choices,
        default=Status.ORDERED,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    purchase_sale_order = models.ManyToManyField(
        "users.User", through="orders.PurchaseSaleOrder", related_name="orders"
    )

    coupon = models.ForeignKey(
        "sales.Coupon",
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
    )

    products = models.ManyToManyField(
        "products.Product",
        through="orders.OrderedProducts",
        related_name="orders",
    )


class OrderedProducts(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="ordered_product",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="order_products",
    )


class PurchaseSaleOrder(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.DO_NOTHING,
        related_name="purchase_sale_orders",
    )
    is_sale_order = models.BooleanField(default=False)
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="purchase_orders",
    )
