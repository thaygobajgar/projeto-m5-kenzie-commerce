from django.urls import path
from orders import views as orders_views
from . import views


urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/orders/", orders_views.OrderView.as_view()),
]
