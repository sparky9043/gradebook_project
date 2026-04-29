from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Course
from .forms import CourseCreationForm

# Create your views here.


class GradebookHomeView(LoginRequiredMixin, TemplateView):
    template_name = "gradebook/home.html"
    login_url = reverse_lazy("accounts:login_view")


class GradbookCoursesView(LoginRequiredMixin, ListView):
    model = Course
    template_name = "gradebook/courses.html"
    context_object_name = "courses"


class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseCreationForm
    template_name = "gradebook/create_course.html"
    success_url = reverse_lazy("gradebook:courses")


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "gradebook/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
