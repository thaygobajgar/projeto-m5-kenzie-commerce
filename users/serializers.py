from rest_framework import serializers
from rest_framework.exceptions import ParseError
from addresses.serializers import AddressSerializer
from addresses.models import Address
from shopping_carts.models import ShoppingCart
from .models import User, UserType


def choices_error_message(choices_class):
    valid_choices = [choice[0] for choice in choices_class.choices]
    message = ", ".join(valid_choices).rsplit(",", 1)

    return "Escolher entre " + " e".join(message) + "."


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

    def update(self, instance: User, validated_data: dict) -> User:
        try:
            address_obj = validated_data.pop("address")
            for key, value in address_obj.items():
                setattr(instance.address, key, value)

                instance.address.save()
        except KeyError:
            ...

        for key, value in validated_data.items():
            if key == "user_type" and value == "Administrador":
                raise ParseError("Não é permitido o usuário ser Administrador")

            setattr(instance, key, value)

            if key == "password":
                instance.set_password(value)

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
