from django.urls import path
from .views import (
    GradebookHomeView,
    # Courses
    CoursesListView,
    CreateCourseView,
    CourseDetailView,
    # Students
    StudentsListView,
)

app_name = "gradebook"

urlpatterns = [
    path("", GradebookHomeView.as_view(), name="home"),
    # Course Views
    path("courses/", CoursesListView.as_view(), name="courses"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/create/", CreateCourseView.as_view(), name="create_course"),
    # Student Views
    path("students/", StudentsListView.as_view(), name="students"),
]
