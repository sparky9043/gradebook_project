from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Course, Student, Enrollment
from .forms import CourseCreationForm

# Create your views here.


class GradebookHomeView(LoginRequiredMixin, TemplateView):
    """Display Landing Page After Login"""

    template_name = "gradebook/home.html"
    login_url = reverse_lazy("accounts:login_view")


class CoursesListView(LoginRequiredMixin, ListView):
    """Display List of courses"""

    model = Course
    template_name = "gradebook/courses.html"
    context_object_name = "courses"

    def get_queryset(self):
        return self.model.objects.filter(teacher=self.request.user)


class CreateCourseView(LoginRequiredMixin, CreateView):
    """Display Create Course Form"""

    model = Course
    form_class = CourseCreationForm
    template_name = "gradebook/create_course.html"
    success_url = reverse_lazy("gradebook:courses")


class CourseDetailView(LoginRequiredMixin, DetailView):
    """Display Course Detail"""

    model = Course
    template_name = "gradebook/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StudentsListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "gradebook/students.html"
    context_object_name = "students"


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "gradebook/student_detail.html"
    context_object_name = "student"
