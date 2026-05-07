from django.urls import path
from .views import (
    GradebookHomeView,
    # Courses
    CoursesListView,
    CreateCourseView,
    CourseDetailView,
    # Students
    StudentsListView,
    StudentDetailView,
    create_student_view,
    enroll_student_view,
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
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student_detail"),
    path("students/create/", create_student_view, name="create_student"),
    path("enroll/", enroll_student_view, name="enroll"),
]
