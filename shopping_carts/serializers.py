from rest_framework import serializers
from .models import ShoppingCart, ProductCarts
from products.models import Product
from orders.models import Order


class ShoppingCartProductSerializer(serializers.ModelSerializer):
    quant = serializers.SerializerMethodField()

    def get_quant(self, obj: Product):
        try:
            quant = (
                obj.product_cart.filter(
                    shopping_cart__user=self.context["request"].user,
                )
                .first()
                .quant
            )

            return quant
        except AttributeError:
            return None

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "quant",
        ]
        read_only_fields = [
            "name",
            "price",
        ]


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
                    orders.products.add(obj)
                    order_product = orders.order_products.filter(
                        order=orders,
                        product=obj,
                    ).first()
                    order_product.quant = (
                        obj.product_cart.filter(
                            shopping_cart__user=self.context["request"].user,
                        )
                        .first()
                        .quant
                    )

                    order_product.save()

                    order_product.product.stock -= order_product.quant

                    order_product.product.save()

                    orders.save()

        instance.products.set([])

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

        product = instance.products.filter(id=product_data.id).first()

        if product:
            quant_data = ProductCarts.objects.filter(
                shopping_cart=instance,
                product=product,
            ).first()
            quant_data.quant += 1

            quant_data.save()

            return instance

        instance.products.add(product_data)

        return instance

    class Meta:
        model = ShoppingCart
        fields = [
            "id",
            "user",
            "products",
        ]
