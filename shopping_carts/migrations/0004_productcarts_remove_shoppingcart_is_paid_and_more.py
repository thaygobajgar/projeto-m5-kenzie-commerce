# Generated by Django 4.1.7 on 2023-03-09 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0004_alter_product_category_alter_product_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shopping_carts", "0003_shoppingcart_is_paid"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductCarts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quant", models.IntegerField(default=1)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_cart",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="shoppingcart",
            name="is_paid",
        ),
        migrations.RemoveField(
            model_name="shoppingcart",
            name="orders",
        ),
        migrations.AlterField(
            model_name="shoppingcart",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shopping_carts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="OrderedCarts",
        ),
        migrations.AddField(
            model_name="productcarts",
            name="shopping_cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cart_products",
                to="shopping_carts.shoppingcart",
            ),
        ),
        migrations.AddField(
            model_name="shoppingcart",
            name="products",
            field=models.ManyToManyField(
                related_name="shopping_carts",
                through="shopping_carts.ProductCarts",
                to="products.product",
            ),
        ),
    ]
