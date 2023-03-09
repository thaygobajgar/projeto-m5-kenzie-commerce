from django.urls import path
from .views import ShoppingCartView, ShoppingCartAddView, ShoppingCartCheckoutView

urlpatterns = [
    path("shopping-cart/", ShoppingCartView.as_view()),
    path(
        "shopping-cart/<int:product_id>/",
        ShoppingCartAddView.as_view(),
    ),
    path("shopping-cart/checkout/", ShoppingCartCheckoutView.as_view()),
]
