from django.urls import path, include
from rest_framework import routers

from . import views as api_views

router = routers.SimpleRouter()
router.register("brand", api_views.BrandApiView, basename="brand")
router.register("category", api_views.CategoryApiView, basename="category")
router.register("product", api_views.ProductApiView, basename="product")

urlpatterns = [
    path("insert-data/", api_views.insert_data, name="insert_data"),
    path("", include(router.urls))
]
