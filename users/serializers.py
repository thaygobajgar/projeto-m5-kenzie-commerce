from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from addresses.serializers import AddressSerializer
from addresses.models import Address


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="This field must be unique."
            )
        ],
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Username already exists"
            )
        ]
    )

    address = AddressSerializer()

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
            "password"
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data: dict):
        address_obj = validated_data.pop('address')
        if validated_data['user_type'] == 'Administrador':
            user_obj = User.objects.create_superuser(**validated_data)
            Address.objects.create(**address_obj, user=user_obj)
            return user_obj

        user_obj = User.objects.create_user(**validated_data)
        Address.objects.create(**address_obj, user=user_obj)
        print(user_obj)
        return user_obj

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
