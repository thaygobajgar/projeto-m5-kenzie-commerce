from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from products.models import Product
from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartAddSerializer
from rest_framework.exceptions import NotFound


class ShoppingCartView(ListAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ShoppingCart.objects.all()

        return ShoppingCart.objects.filter(user=self.request.user)


class ShoppingCartAddView(UpdateAPIView):
    serializer_class = ShoppingCartAddSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        shopping_cart_object = ShoppingCart.objects.filter(
            user=self.request.user
        ).first()

        product = get_object_or_404(Product, id=self.kwargs["product_id"])
        self.request.product = product

        return shopping_cart_object


class ShoppingCartCheckoutView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ShoppingCartSerializer

    def get_object(self):
        user = self.request.user
        shopping_cart_object = ShoppingCart.objects.filter(user=user).first()

        if not shopping_cart_object.products.all():
            raise NotFound("sem produtos no carrinho")

        for obj in shopping_cart_object.products.all():
            if not obj.is_avaiable:
                raise NotFound(f"{obj.name} indisponivel")

            quant = obj.product_cart.filter(
                shopping_cart__user=user,
            ).count()

            if obj.stock < quant:
                raise NotFound(
                    f"quantidade do {obj.name} indisponível",
                )

        return shopping_cart_object
