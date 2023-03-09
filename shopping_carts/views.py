from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartAddSerializer
from rest_framework.exceptions import NotFound
from orders.models import Order


class ShoppingCartView(ListCreateAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ShoppingCart.objects.all()

        return ShoppingCart.objects.filter(user=self.request.user, is_paid=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShoppingCartAddView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ShoppingCartAddSerializer
    lookup_url_kwarg = "shopping_cart_id"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ShoppingCart.objects.all()

        return ShoppingCart.objects.filter(account=self.request.user, is_paid=False)

    def perform_create(self, serializer):
        product_id = self.kwargs["product_id"]
        shopping_cart_object = ShoppingCart.objects.filter(
            user=self.request.user, is_paid=False
        ).first()
        serializer.save(product_id=product_id, shopping_cart=shopping_cart_object)


class ShoppingCartCheckoutView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    # serializer_class =

    def get_object(self):
        shopping_cart_object = ShoppingCart.objects.filter(
            user=self.request.user, is_paid=False
        ).first()

        # for obj in shopping_cart_object.orders.all():
        #     if not obj.is_avaiable:
        #         raise NotFound("produto indisponivel")

        if not shopping_cart_object:
            raise NotFound

        seller_set = {obj.user for obj in shopping_cart_object.orders.all()}

        for seller in seller_set:
            import ipdb

            ipdb.set_trace()
            orders = Order.objects.create(user=seller)
            for obj in shopping_cart_object.orders.all():
                if obj.user == seller:
                    orders.product.add(obj)

        # shopping_cart_object.is_paid = True
        # shopping_cart_object.save()
        # return shopping_cart_object
