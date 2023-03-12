from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthEmployee, IsEmployeeOrReadOnly, IsAuthAdminOrReadyOnly
from .serializers import UserSerializer
from rest_framework import generics


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthAdminOrReadyOnly]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAuthEmployee]

    queryset = User.objects.all()
    serializer_class = UserSerializer
