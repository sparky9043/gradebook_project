from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Course, Student, Enrollment
from .forms import CourseCreationForm
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
)
from django.contrib import messages
from bokeh.models import ColumnDataSource
from bokeh.palettes import Bright6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.embed import components

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
        enrollments = Enrollment.objects.filter(course=self.get_object())
        context["enrollments"] = enrollments
        return context


class CourseStatsView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "gradebook/course_stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get all enrollments to  the course
        enrollments = Enrollment.objects.filter(course=self.get_object())
        context["enrollments"] = enrollments
        # filter grades and grade count only
        grades_only = [enrollment.final_grade for enrollment in enrollments]
        grades_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for grade in grades_only:
            if grade:
                grades_count[grade] += 1

        grades = [*grades_count]
        counts = [*grades_count.values()]

        # def convert_letter_to_number(letter_grade: str):
        #     if letter_grade == "A":
        #         return 4
        #     if letter_grade == "B":
        #         return 3
        #     if letter_grade == "C":
        #         return 2
        #     if letter_grade == "D":
        #         return 1
        #     return 0

        #  Graph logic starts here
        source = ColumnDataSource(data=dict(grades=grades, counts=counts))

        p = figure(
            x_range=grades,
            height=350,
            toolbar_location=None,
            title="Grade Distribution",
        )

        p.vbar(
            x="grades",
            top="counts",
            width=0.9,
            source=source,
            legend_field="grades",
            line_color="white",
            fill_color=factor_cmap("grades", palette=Bright6, factors=grades),
        )

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = 9
        p.legend.orientation = "horizontal"
        p.legend.location = "top_center"

        script, div = components(p)

        context["script"] = script
        context["div"] = div
        context["show_bokeh"] = True

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
        # Courses by the current teacher
        courses_queryset = self.request.user.courses.all()
        courses = [course.title for course in courses_queryset]
        context["courses"] = courses
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

    if request.method == "POST":
        course_name = request.POST.get("course")
        course = Course.objects.get(title=course_name)
        if not course:
            messages.error(request, "there are no courses by that name")
            return HttpResponseBadRequest("")

        if course.teacher.username != request.user.username:
            messages.error(request, "Teacher does not have access to this course")
            return HttpResponseBadRequest("")

        try:
            enrollment = Enrollment.objects.create(
                student=student,
                course=course,
            )
            print(enrollment)
        except:
            messages.error(request, "The student is already enrolled in the course")
            return redirect("gradebook:student_detail", pk=pk)

        messages.success(
            request, f"{enrollment.student} enrolled to {enrollment.course.title}"
        )
        return redirect("gradebook:student_detail", pk=pk)
    else:
        return HttpResponseRedirect(reverse(""))
