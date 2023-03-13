from rest_framework import serializers
from django.core.mail import send_mail

from .models import Order
from products.models import Product
from users.serializers import UserSerializer


def dispatch_email(status, buyer, products):
    subject = f"O status do seu pedido foi atualizado para {status}"
    message = f"Olá {buyer}, O status do seu pedido foi atualizado para {status}.\n\nDetalhes do pedido:\n"
    for produto in products:
        message += f"Nome do produto: {produto.nome}\nDescrição: {produto.descricao}\nPreço: {produto.preco}\n\n"
    recipient_list = [buyer.email]
    send_mail(
        subject, message, "rikellyh898@gmail.com", recipient_list, fail_silently=False
    )


class OrderProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    def get_category_name(self, obj: Product) -> str:
        category_name = obj.category.name

        return category_name

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "is_avaiable",
            "price",
            "description",
            "category_name",
            "product_image",
            "user",
        ]

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        user = instance.user
        product = instance.product.all()
        instance = super().update(instance, validated_data)

        if status != instance.status:
            dispatch_email(status, user, product)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True,
    )
    client = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()

    def get_client(self, obj: Order) -> str:
        client = (
            obj.purchase_sale_order.filter(
                purchase_sale_orders__is_sale_order=False,
            )
            .first()
            .username
        )

        return client

    def get_seller(self, obj: Order) -> str:
        seller = (
            obj.purchase_sale_order.filter(
                purchase_sale_orders__is_sale_order=True,
            )
            .first()
            .username
        )

        return seller

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "created_at",
            "client",
            "seller",
            "products",
        ]

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        user = instance.user
        product = instance.product.all()
        instance = super().update(instance, validated_data)

        if status != instance.status:
            dispatch_email(status, user, product)
        return instance
