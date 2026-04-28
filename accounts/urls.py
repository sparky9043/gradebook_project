from django.urls import path
from .views import (
    TeacherLoginView,
    TeacherLogoutView,
    TeacherRegisterView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", TeacherLoginView.as_view(), name="login_view"),
    path("register/", TeacherRegisterView.as_view(), name="register_view"),
    path("logout/", TeacherLogoutView.as_view(), name="logout_view"),
]
