from rest_framework import serializers
from .models import ShoppingCart, ProductCarts
from products.models import Product
from orders.models import Order, OrderedProducts


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
        ]
        read_only_fields = fields


class ShoppingCartSerializer(serializers.ModelSerializer):
    products = ShoppingCartProductSerializer(
        read_only=True,
        many=True,
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    def update(self, instance: ShoppingCart, validated_data: dict):
        seller_set = {obj.user for obj in instance.products.all()}

        for seller in seller_set:
            orders = Order.objects.create(user=seller)
            for obj in instance.products.all():
                if obj.user == seller:
                    OrderedProducts.objects.create(
                        product=obj,
                        order=orders,
                    )

                    product = instance.products.filter(id=obj.id).first()

                    product.stock -= 1

                    if not product.stock:
                        product.is_avaiable = False

                    product.save()

        instance.products.clear()

        instance.save()

        return instance

    class Meta:
        model = ShoppingCart
        fields = [
            "id",
            "user",
            "products",
        ]


class ShoppingCartAddSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    products = ShoppingCartProductSerializer(
        read_only=True,
        many=True,
    )

    def update(self, instance: ShoppingCart, validated_data: dict):
        product_data = self.context["request"].product

        ProductCarts.objects.create(
            product=product_data,
            shopping_cart=instance,
        )

        return instance

    class Meta:
        model = ShoppingCart
        fields = [
            "id",
            "user",
            "products",
        ]
