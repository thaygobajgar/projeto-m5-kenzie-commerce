from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=127)
    stock = models.IntegerField(default=0)
    is_avaiable = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(
        "categories.Category", on_delete=models.DO_NOTHING, related_name="products"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.DO_NOTHING, related_name="products"
    )
