from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound
from products.models import Product
from sales.models import Coupon
from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartAddSerializer


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
        coupon_data = self.request.data.get("coupon")

        if coupon_data:
            coupon = Coupon.objects.filter(
                name__iexact=coupon_data,
                is_avaiable=True,
            ).first()

            if not coupon:
                raise NotFound("Cupom não está válido")

            if coupon.validity == date.today():
                coupon.is_avaiable = False
                coupon.save()

                raise NotFound("Cupom não está válido")

            self.request.coupon = coupon

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
