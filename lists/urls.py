from django.urls import path
from .views import (
    ListView,
    ListDetailView,
    ListRemoveProductView,
)

urlpatterns = [
    path("lists/", ListView.as_view()),
    path("lists/<int:list_id>/", ListDetailView.as_view()),
    path(
        "lists/<int:list_id>/add/<int:product_id>/",
        ListDetailView.as_view(),
    ),
    path(
        "lists/<int:list_id>/remove/<int:product_id>/",
        ListRemoveProductView.as_view(),
    ),
]
