from django.urls import path
from .views import GradebookHomeView

app_name = "gradebook"

urlpatterns = [
    path("", GradebookHomeView.as_view(), name="home"),
    # path("courses/")
]
