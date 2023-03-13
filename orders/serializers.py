from rest_framework import serializers
from django.core.mail import send_mail

from .models import Order
from products.serializers import ProductSerializer
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


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "product", "date", "status", "user"]

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        user = instance.user
        product = instance.product.all()
        instance = super().update(instance, validated_data)

        if status != instance.status:
            dispatch_email(status, user, product)
        return instance
