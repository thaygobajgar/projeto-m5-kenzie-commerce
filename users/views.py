from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthEmployee, IsEmployeeOrReadOnly, IsAdminOrAccountOwner
from .serializers import UserSerializer
from rest_framework import generics


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsEmployeeOrReadOnly]


class UserDetailView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrAccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer
