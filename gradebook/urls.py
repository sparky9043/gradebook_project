from django.urls import path
from .views import (
    GradebookHomeView,
    # Courses
    CoursesListView,
    CreateCourseView,
    CourseDetailView,
    CourseDeleteView,
    CourseStatsView,
    # Students
    StudentsListView,
    StudentSearchView,
    StudentDetailView,
    create_student_view,
    enroll_student_view,
    StudentEnrollFinalGrade,
    StudentEditView,
    StudentDeleteView,
    # Stats View
    StatsView,
)

app_name = "gradebook"

urlpatterns = [
    path("", GradebookHomeView.as_view(), name="home"),
    # Course Views
    path("courses/", CoursesListView.as_view(), name="courses"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/<int:pk>/stats", CourseStatsView.as_view(), name="course_stats"),
    path("courses/<int:pk>/delete", CourseDeleteView.as_view(), name="course_delete"),
    path("courses/create/", CreateCourseView.as_view(), name="create_course"),
    # Student Views
    path("students/", StudentsListView.as_view(), name="students"),
    path("students/search", StudentSearchView.as_view(), name="student_search"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student_detail"),
    path("students/<int:pk>/enroll", enroll_student_view, name="enroll"),
    path("students/<int:pk>/edit", StudentEditView.as_view(), name="student_edit"),
    path(
        "students/<int:pk>/delete", StudentDeleteView.as_view(), name="student_delete"
    ),
    path("students/create/", create_student_view, name="create_student"),
    # Enrollment Views
    path(
        "enrollments/<int:pk>/add-grade/",
        StudentEnrollFinalGrade.as_view(),
        name="enroll_final_grade",
    ),
    # Stats View
    path("stats/", StatsView.as_view(), name="stats"),
]
