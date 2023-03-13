from .models import Order
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAuthEmployee
from .serializers import OrderSerializer
from rest_framework import generics


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
