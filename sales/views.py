from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Coupon
from .serializers import CouponSerializer, CouponDisabledSerializer


class CouponView(ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CouponDetailView(UpdateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CouponDisabledView(UpdateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponDisabledSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
