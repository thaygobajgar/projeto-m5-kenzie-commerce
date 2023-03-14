from django.db import models


class Coupon(models.Model):
    name = models.CharField(max_length=127)
    discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )
    created_at = models.DateField(auto_now_add=True)
    is_avaiable = models.BooleanField(default=True)
    validity = models.DateField(null=True)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="coupons",
    )
