from django.urls import path
from .views import (
    ListView,
    ListDetailView,
    ListAddProductView,
    ListRemoveProductView,
)

urlpatterns = [
    path("lists/", ListView.as_view()),
    path("lists/<int:pk>/", ListDetailView.as_view()),
    path("lists/<int:pk>/add/", ListAddProductView.as_view()),
    path("lists/<int:pk>/remove/", ListRemoveProductView.as_view()),
]
