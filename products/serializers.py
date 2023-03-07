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

        product = Product.objects.create(
            **validated_data,
            category=category,
        )

        return product

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
