from django.urls import path
from .views import CouponView, CouponDetailView, CouponDisabledView

urlpatterns = [
    path("sales/coupons/", CouponView.as_view()),
    path("sales/coupons/<int:pk>/", CouponDetailView.as_view()),
    path("sales/coupons/<int:pk>/disabled/", CouponDisabledView.as_view()),
]
