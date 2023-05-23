from django.urls import path
from .views import CustomUserRegistration

app_name = "users"

urlpatterns = [
    path("register/", CustomUserRegistration.as_view(), name="create_user")
]
