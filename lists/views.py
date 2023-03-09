from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    UpdateAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from .models import List
from .permissions import IsAccountOwner
from .serializers import (
    ListSerializer,
    ListAddProductSerializer,
    ListRemoveProductSerializer,
)


class ListView(ListCreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return List.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(
            user=self.request.user,
        )


class ListDetailView(RetrieveDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]


class ListAddProductView(UpdateAPIView):
    queryset = List.objects.all()
    serializer_class = ListAddProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]


class ListRemoveProductView(UpdateAPIView):
    queryset = List.objects.all()
    serializer_class = ListRemoveProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwner]


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
