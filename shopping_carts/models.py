from django.db import models

# Create your models here.


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.DO_NOTHING, related_name="shopping_carts"
    )
    orders = models.ManyToManyField(
        "products.Product",
        through="shopping_carts.OrderedCarts",
        related_name="ordered_products",
    )
    is_paid = models.BooleanField(default=False)


class OrderedCarts(models.Model):
    product = models.ForeignKey(
        "products.Product", on_delete=models.DO_NOTHING, related_name="ordered_product"
    )
    shopping_cart = models.ForeignKey(
        "shopping_carts.ShoppingCart",
        on_delete=models.DO_NOTHING,
        related_name="cart_products_order",
    )
