from rest_framework import serializers
from products.models import Product
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    product = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "review",
            "user",
            "product",
        ]
