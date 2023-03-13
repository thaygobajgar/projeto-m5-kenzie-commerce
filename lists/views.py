from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from products.models import Product
from .models import List
from .permissions import IsAccountOwner
from .serializers import (
    ListSerializer,
    ListRemoveProductSerializer,
)


class ListView(ListCreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return List.objects.all()

        return List.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user,
        )


class ListDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]
    lookup_url_kwarg = "list_id"

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")

        if product_id:
            if Product.objects.filter(
                lists=self.kwargs["list_id"],
                id=product_id,
            ).first():
                raise ParseError("Produto já adicionado")

            product = get_object_or_404(Product, id=product_id)

            self.request.product = product

        return List.objects.all()


class ListRemoveProductView(UpdateAPIView):
    serializer_class = ListRemoveProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]
    lookup_url_kwarg = "list_id"

    def get_queryset(self):
        product = get_object_or_404(Product, id=self.kwargs["product_id"])

        if not product.lists.filter(id=self.kwargs["list_id"]).first():
            raise NotFound("esse produto não consta na lista")

        self.request.product = product

        return List.objects.all()


class ListWithProductView(CreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, id=self.kwargs["pk"])
        self.request.product = product

        return serializer.save(
            user=self.request.user,
        )
