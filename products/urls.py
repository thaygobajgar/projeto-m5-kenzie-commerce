from django.urls import path
from reviews.views import ReviewView
from lists.views import ListWithProductView
from .views import ProductView, ProductDetailView

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("products/<int:pk>/reviews/", ReviewView.as_view()),
    path("products/<int:pk>/lists/", ListWithProductView.as_view()),
]
