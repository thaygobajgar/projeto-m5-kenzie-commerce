from statistics import mean
from rest_framework import serializers
from categories.models import Category
from categories.serializers import CategorySerializer
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(write_only=True)
    category_name = serializers.SerializerMethodField()
    stars = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    def get_category_name(self, obj: Product) -> str:
        category_name = obj.category.name

        return category_name

    def get_stars(self, obj: Product) -> float | None:
        reviews = obj.reviews.all()
        stars = [review.stars for review in reviews]

        if not stars:
            return None

        return round(mean(stars), 1)

    def get_reviews_count(self, obj: Product) -> int:
        reviews_count = obj.reviews.count()

        return reviews_count

    def create(self, validated_data: dict) -> Product:
        category_data = validated_data.pop("category")
        category = Category.objects.filter(
            name__iexact=category_data["name"],
        ).first()

        if not category:
            category = Category.objects.create(**category_data)

        stock = validated_data.get("stock", 0)

        if stock:
            validated_data["is_avaiable"] = True

        product = Product.objects.create(
            **validated_data,
            category=category,
        )

        return product

    def update(self, instance: Product, validated_data: dict) -> Product:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        if instance.stock:
            instance.is_avaiable = True

        instance.save()

        return instance

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "stock",
            "is_avaiable",
            "price",
            "description",
            "category_name",
            "stars",
            "reviews_count",
            "category",
        ]
