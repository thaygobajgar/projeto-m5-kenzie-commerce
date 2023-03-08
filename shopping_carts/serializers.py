from rest_framework import serializers
from .models import ShoppingCart, OrderedCarts
from products.serializers import ProductSerializer


class ShoppingCartSerializer(serializers.Serializer):
    class Meta:
        model = ShoppingCart
        fields = [
            "id",
            "user",
            "orders",
            "is_paid",
            "cart_products_order",
        ]

    def create(self, validated_data):
        shopping_cart_obj = ShoppingCart.objects.create(**validated_data)

        return shopping_cart_obj


class ShoppingCartAddSerializer(serializers.Serializer):
    product = ProductSerializer(read_only=True)
    shopping_cart = ShoppingCartSerializer(read_only=True)

    class Meta:
        model = OrderedCarts
        fields = ["id", "product", "shopping_cart"]

    def create(self, validated_data):
        ordered_cart_obj = OrderedCarts.objects.create(**validated_data)
        import ipdb

        ipdb.set_trace()
        return ordered_cart_obj
