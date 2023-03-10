from rest_framework import serializers
from rest_framework.views import Response, status
from addresses.serializers import AddressSerializer
from addresses.models import Address
from shopping_carts.models import ShoppingCart
from .models import User, UserType


def choices_error_message(choices_class):
    valid_choices = [choice[0] for choice in choices_class.choices]
    message = ", ".join(valid_choices).rsplit(",", 1)

    return "Escolher entre " + "e".join(message) + "."


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    def create(self, validated_data: dict):
        address_obj = validated_data.pop("address")
        if validated_data.get("user_type") == "Administrador":
            user_obj = User.objects.create_superuser(**validated_data)
            Address.objects.create(**address_obj, user=user_obj)
            return user_obj

        user_obj = User.objects.create_user(**validated_data)
        Address.objects.create(**address_obj, user=user_obj)
        ShoppingCart.objects.create(user=user_obj)

        return user_obj

    def update(self, instance: User, validated_data: dict):
        if validated_data['user_type'] == "Administrador":
            raise PermissionError("You don't have permission to do this")
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "user_type",
            "email",
            "first_name",
            "last_name",
            "address",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "user_type": {
                "error_messages": {
                    "invalid_choice": choices_error_message(UserType),
                }
            },
        }
