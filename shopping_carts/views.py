from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ShoppingCart
from .serializers import ShoppingCartSerializer, ShoppingCartAddSerializer


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
