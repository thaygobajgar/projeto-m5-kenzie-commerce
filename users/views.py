from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsAdminOrAccountOwner
from .serializers import UserSerializer
from rest_framework import generics


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrAccountOwner]


class UserDetailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrAccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer
