from django.db import models

# Create your models here.


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="shopping_carts",
    )
    products = models.ManyToManyField(
        "products.Product",
        through="shopping_carts.ProductCarts",
        related_name="shopping_carts",
    )


class ProductCarts(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="product_cart",
    )
    shopping_cart = models.ForeignKey(
        "shopping_carts.ShoppingCart",
        on_delete=models.CASCADE,
        related_name="cart_products",
    )
    quant = models.IntegerField(default=1)
