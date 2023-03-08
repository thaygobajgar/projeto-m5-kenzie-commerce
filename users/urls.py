from django.urls import path
from orders import views as orders_views
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/orders/", orders_views.OrderView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
]
