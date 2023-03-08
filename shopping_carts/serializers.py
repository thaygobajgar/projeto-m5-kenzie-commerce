from rest_framework import serializers
from .models import ShoppingCart, OrderedCarts
from products.serializers import ProductSerializer


class CartProductOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderedCarts
        fields = ["id", "product", "shopping_cart"]
        read_only_fields = ["shopping_cart"]


class ShoppingCartSerializer(serializers.ModelSerializer):
    orders = CartProductOrderSerializer(read_only=True, many=True)

    class Meta:
        model = ShoppingCart
        fields = [
            "id",
            "user",
            "is_paid",
            "orders",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        shopping_cart_obj = ShoppingCart.objects.create(**validated_data)

        return shopping_cart_obj


class ShoppingCartAddSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    shopping_cart = ShoppingCartSerializer(read_only=True)

    class Meta:
        model = OrderedCarts
        fields = ["id", "product", "shopping_cart"]

    def create(self, validated_data):
        ordered_cart_obj = OrderedCarts.objects.create(**validated_data)

        return ordered_cart_obj
