from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "review",
            "product",
        ]
