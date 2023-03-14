from rest_framework import serializers
from .models import Coupon
from datetime import date


class CouponSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    def create(self, validated_data: dict) -> Coupon:
        coupon = Coupon.objects.filter(
            name__iexact=validated_data["name"],
        ).first()

        if not coupon:
            coupon = Coupon.objects.create(**validated_data)

        return coupon

    def update(self, instance: Coupon, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

            if key == "validity":
                if value > date.today():
                    instance.is_avaiable = True

        instance.save()

        return instance

    class Meta:
        model = Coupon
        fields = [
            "id",
            "name",
            "discount",
            "created_at",
            "is_avaiable",
            "validity",
            "user",
        ]


class CouponDisabledSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
    )

    def update(self, instance: Coupon, validated_data: dict):
        instance.is_avaiable = False
        instance.validity = date.today()

        instance.save()

        return instance

    class Meta:
        model = Coupon
        fields = [
            "id",
            "name",
            "discount",
            "created_at",
            "is_avaiable",
            "validity",
            "user",
        ]
