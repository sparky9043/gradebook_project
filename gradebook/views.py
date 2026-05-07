from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib import messages

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
        students = Student.objects.all().order_by("grade_level", "last_name")
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


@login_required
def create_student_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            dob = request.POST.get("dob")
            if not first_name or not last_name or not dob:
                raise ValueError("Please fill out all the fields")

            grade_level = request.POST.get("grade_level")
            new_student = Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                dob=dob,
                grade_level=grade_level,
            )
            messages.success(request, f"Student: {first_name} {last_name} Created!")
            return redirect("gradebook:students")
        except ValueError as e:
            messages.error(request, e)
            return redirect("gradebook:students")
    else:
        return HttpResponseBadRequest("400 Bad Request")


@login_required
def enroll_student_view(request: HttpResponse, pk) -> HttpRequest:
    student = get_object_or_404(Student, pk=pk)
    course_query_set = request.user.courses.all()
    courses = [course.title for course in list(course_query_set)]
    context = {"courses": courses}
    if request.method == "GET":
        return render(request, "gradebook/enrollment.html", context)

    if request.method == "POST":
        course_name = request.POST.get("course")
        course = Course.objects.get(title=course_name)
        if not course:
            messages.error(request, "there are no courses by that name")
            return HttpResponseBadRequest("")

        try:
            enrollment = Enrollment.objects.create(
                student=student,
                course=course,
            )
            print(enrollment)
        except:
            messages.error(request, "The student is already enrolled in the course")
            return render(request, "gradebook/enrollment.html", context)

        return redirect("gradebook:student_detail", pk=pk)
