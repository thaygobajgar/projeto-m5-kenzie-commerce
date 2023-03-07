from rest_framework import serializers
from categories.models import Category
from categories.serializers import CategorySerializer
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    def create(self, validated_data: dict):
        category_data = validated_data.pop("category")
        category = Category.objects.filter(
            name__iexact=category_data["name"],
        ).first()

        if not category:
            category = Category.objects.create(**category_data)

        stock = validated_data.get("stock", 0)

        if stock:
            validated_data["is_avaiable"] = True

        product = Product.objects.create(
            **validated_data,
            category=category,
        )

        return product

    def update(self, instance: Product, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if instance.stock:
            instance.is_avaiable = True

        instance.save()

        return instance

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "stock",
            "is_avaiable",
            "price",
            "description",
            "category",
        ]
