# Generated by Django 4.1.7 on 2023-03-10 16:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_orderedproducts_order_products"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderedproducts",
            name="quant",
        ),
    ]
