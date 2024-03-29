from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from products.models import Product
from .models import Review
from .serializers import ReviewSerializer


class ReviewView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        product = get_object_or_404(
            Product,
            id=self.kwargs["pk"],
        )

        return serializer.save(
            product=product,
            user=self.request.user,
        )
