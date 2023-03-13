from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from products.models import Product
from .models import Order, Status


def choices_error_message(choices_class):
    valid_choices = [choice[0] for choice in choices_class.choices]
    message = ", ".join(valid_choices).rsplit(",", 1)

    return "Escolher entre " + " e".join(message) + "."


def dispatch_email(status, buyer, products):
    subject = f"O status do seu pedido foi atualizado para {status}"
    message = f"Olá {buyer.first_name}, O status do seu pedido foi atualizado para {status}.\n\nDetalhes do pedido:\n"
    for product in products:
        message += f"Nome do produto: {product.name}\nDescrição: {product.description}\nPreço: {product.price}\n\n"
    recipient_list = [buyer.email]
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
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

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        user = instance.purchase_sale_order.filter(
            purchase_sale_orders__is_sale_order=False,
        ).first()
        products = instance.products.all()

        if status != instance.status:
            dispatch_email(status, user, products)
            instance.status = status

        instance.save()

        return instance

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
        extra_kwargs = {
            "status": {
                "error_messages": {
                    "invalid_choice": choices_error_message(Status),
                }
            },
        }
