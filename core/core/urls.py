from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("retail.urls", namespace="retail")),
    path("api/user/", include("users.urls", namespace="users"))
]
