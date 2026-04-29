from django.urls import path
from .views import (
    GradebookHomeView,
    GradbookCoursesView,
    CreateCourseView,
    CourseDetailView,
)

app_name = "gradebook"

urlpatterns = [
    path("", GradebookHomeView.as_view(), name="home"),
    path("courses/", GradbookCoursesView.as_view(), name="courses"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/create/", CreateCourseView.as_view(), name="create_course"),
]
