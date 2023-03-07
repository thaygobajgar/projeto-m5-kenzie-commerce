from django.urls import path
from reviews.views import ReviewView
from .views import ProductView, ProductDetailView

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("products/<int:pk>/reviews/", ReviewView.as_view()),
]
