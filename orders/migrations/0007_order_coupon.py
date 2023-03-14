# Generated by Django 4.1.7 on 2023-03-14 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("sales", "0001_initial"),
        ("orders", "0006_order_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="coupon",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="sales.coupon",
            ),
        ),
    ]
