# Generated by Django 4.1.7 on 2023-03-06 17:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_client",
        ),
    ]
