from django.urls import path
from .views import (
    index,
    # DashboardView,
)

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    # path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
