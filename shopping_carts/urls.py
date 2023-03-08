from django.urls import path
from .views import ShoppingCartView, ShoppingCartAddView

urlpatterns = [
    path("shopping-cart/", ShoppingCartView.as_view()),
    path(
        "shopping-cart/<int:shopping_cart_id>/add/<int:product_id>/",
        ShoppingCartAddView.as_view(),
    ),
    path("shopping-cart/checkout/", ShoppingCartView.as_view()),
]
