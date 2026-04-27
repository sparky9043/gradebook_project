from django.urls import path
from .views import register_view, TeacherLoginView

app_name = "accounts"

urlpatterns = [
    path("login/", TeacherLoginView.as_view(), name="login_view"),
    path("register/", register_view, name="register_view"),
]
