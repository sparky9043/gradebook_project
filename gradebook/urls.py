from django.urls import path
from .views import GradeLogMainView

app_name = "gradebook"

urlpatterns = [
    path("", GradeLogMainView.as_view(), name="home"),
]
