from django.shortcuts import render, redirect
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
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest

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

    def get_queryset(self):
        students = Student.objects.all().order_by("grade_level")
        return students


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "gradebook/student_detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context["records"] = student.enrollments.filter(student=student).distinct()
        return context


# class CreateStudentView(LoginRequiredMixin, CreateView):
#     model = Student
#     context_object_name = "student"
#     success_url = reverse_lazy("gradebook:students")
@login_required
def create_student_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        dob = request.POST.get("dob")
        grade_level = request.POST.get("grade_level")

        try:
            new_student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                grade_level=grade_level,
            )
            return redirect("gradebook:students")
        except ValueError:
            print("invalid error")
            return redirect("gradebook:students")
    else:
        return HttpResponseBadRequest("400 Bad Request")
