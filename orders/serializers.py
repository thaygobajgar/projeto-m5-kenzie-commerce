from rest_framework import serializers

from .models import Order
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "users_id"]

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
