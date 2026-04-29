from django.urls import path
from .views import GradebookHomeView, GradbookCoursesView

app_name = "gradebook"

urlpatterns = [
    path("", GradebookHomeView.as_view(), name="home"),
    path("courses/", GradbookCoursesView.as_view(), name="courses"),
]
