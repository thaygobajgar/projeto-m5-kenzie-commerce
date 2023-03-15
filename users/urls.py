from django.urls import path

from . import views
from rest_framework_simplejwt import views as jwt_views
from orders import views as orders_views


urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
    path("users/orders/", orders_views.OrderView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
]
