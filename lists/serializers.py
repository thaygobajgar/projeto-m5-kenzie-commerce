from django.shortcuts import get_object_or_404
from rest_framework import serializers
from products.serializers import ProductSerializer
from products.models import Product
from .models import List


class ListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    products = ProductSerializer(
        read_only=True,
        many=True,
    )

    def create(self, validated_data: dict):
        list_data = List.objects.filter(
            name__iexact=validated_data["name"],
            user=self.context["request"].user,
        ).first()

        if not list_data:
            list_data = List.objects.create(**validated_data)

        try:
            product = self.context["request"].product
            list_data.products.add(product)

            return list_data
        except AttributeError:
            return list_data

    class Meta:
        model = List
        fields = [
            "id",
            "name",
            "products",
            "user",
        ]


class ListAddProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    def update(self, instance: List, validated_data: list):
        for product in validated_data["products"]:
            instance.products.add(product)

        instance.save()

        return instance

    class Meta:
        model = List
        fields = [
            "id",
            "name",
            "products",
            "user",
        ]


class ListRemoveProductSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    def update(self, instance: List, validated_data: list):
        for product in validated_data["products"]:
            instance.products.remove(product)

        instance.save()

        return instance

    class Meta:
        model = List
        fields = [
            "id",
            "name",
            "products",
            "user",
        ]
