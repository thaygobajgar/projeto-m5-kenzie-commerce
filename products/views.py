from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from .models import Product
from .serializers import ProductSerializer


class ProductView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
