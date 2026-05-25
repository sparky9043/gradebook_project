from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Course, Student, Enrollment
from .forms import CourseCreationForm, StudentCreationForm
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseForbidden,
)
from django.contrib import messages
from .helpers import (
    get_pie_graph,
    convert_number_to_letter,
    calculate_gpa,
    get_bar_graph,
)
from django.db.models import Q
from django.core.paginator import Paginator


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
        if self.request.user.is_superuser:
            return self.model.objects.all().order_by("teacher__last_name", "title")

        return self.model.objects.filter(teacher=self.request.user)


class CreateCourseView(LoginRequiredMixin, CreateView):
    """Display Create Course Form"""

    model = Course
    form_class = CourseCreationForm
    template_name = "gradebook/create_course.html"
    success_url = reverse_lazy("gradebook:courses")

    def form_valid(self, form):
        messages.success(self.request, "Course created!")
        return super().form_valid(form)


class CourseDetailView(LoginRequiredMixin, DetailView):
    """Display Course Detail"""

    model = Course
    template_name = "gradebook/course_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != self.get_object().teacher.username:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)

            messages.error(request, "You do not have access to view this course")
            return render(request, "403.html", status=403)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get records for only the specific course
        enrollments = Enrollment.objects.filter(course=self.get_object())
        # Sort by student last name
        sorted_enrollments = sorted(
            enrollments,
            key=lambda e: e.student.last_name,
        )
        # create paginator with sorted elements and 10 items per page
        paginator = Paginator(sorted_enrollments, 10)
        # get page request according to <a href="?page={{ page_obj.next_page_number }}"
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["total_enrollments"] = enrollments.count()
        context["page_obj"] = page_obj
        context["paginator"] = paginator
        return context


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "gradebook/course_delete.html"
    success_url = reverse_lazy("gradebook:courses")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            messages.error(request, "You do not have access to view this page")
            return render(request, "403.html", status=403)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_superuser:
            messages.success(self.request, "Course deleted")
            return super().form_valid(form)
        else:
            messages.error(
                self.request, "You do not have the permission to delete the course"
            )
            super().form_invalid(form)
            return redirect(
                reverse(
                    "gradebook:course_detail",
                    kwargs={"pk": self.get_object().pk},
                )
            )


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

        script, div = get_pie_graph(grades_count)

        context["script"] = script
        context["div"] = div
        context["show_bokeh"] = True
        context["gpa"] = {
            "points": f"{calculate_gpa(grades_count):.2f}",
            "letter_grade": convert_number_to_letter(
                calculate_gpa(grades_count),
            ),
        }

        return context


class StudentsListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "gradebook/students.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):
        students = Student.objects.all().order_by("last_name")
        return students


class StudentSearchView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "gradebook/partials/students_table.html"
    paginate_by = 10
    context_object_name = "students"

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        qs = Student.objects.all().order_by("last_name")
        if q:
            qs = qs.filter(
                Q(first_name__icontains=q) | Q(last_name__icontains=q)
            ).distinct()
        return qs


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "gradebook/student_detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context["records"] = student.enrollments.filter(student=student).distinct()
        # Courses by the current teacher

        if self.request.user.is_superuser:
            courses_queryset = Course.objects.all().order_by("title")
        else:
            courses_queryset = self.request.user.courses.all().order_by("title")

        courses = [course.title for course in courses_queryset]
        already_enrolled = list(course.title for course in student.courses.all())
        # Filter courses that student is already enrolled in
        context["courses"] = [
            course for course in courses if course not in already_enrolled
        ]
        return context


class StudentEditView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentCreationForm
    template_name = "gradebook/student_edit.html"
    success_url = reverse_lazy("gradebook:students")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            messages.error(request, "You do not have access to view this page")
            return render(request, "403.html", status=403)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        student = self.get_object()
        messages.success(
            self.request, f"{student.first_name} {student.last_name} edit successful!"
        )
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "gradebook/student_delete.html"
    success_url = reverse_lazy("gradebook:students")

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            messages.error(request, "You do not have access to view this page")
            return render(request, "403.html", status=403)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_superuser:
            messages.success(self.request, "Student deleted")
            return super().form_valid(form)
        else:
            messages.error(
                self.request, "You do not have the permission to delete the student"
            )
            super().form_invalid(form)
            return redirect(
                reverse(
                    "gradebook:student_detail",
                    kwargs={"pk": self.get_object().pk},
                )
            )


class StudentEnrollFinalGrade(LoginRequiredMixin, UpdateView):
    model = Enrollment
    fields = ["final_grade"]
    template_name = "gradebook/enroll_student_final_grade.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.username != self.get_object().course.teacher.username:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            messages.error(
                request, "You do not have access to edit this student's grade"
            )
            return render(request, "403.html", status=403)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        student_pk = self.get_object().student.pk
        return reverse_lazy("gradebook:student_detail", kwargs={"pk": student_pk})


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
            messages.success(
                request,
                f"Student: {new_student.first_name} {new_student.last_name} Created!",
            )
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
            if not request.user.is_superuser:
                messages.error(request, "Teacher does not have access to this course")
                return render(request, "403.html", status=403)

        try:
            enrollment = Enrollment.objects.create(
                student=student,
                course=course,
            )
        except:
            messages.error(request, "The student is already enrolled in the course")
            return redirect("gradebook:student_detail", pk=pk)

        messages.success(
            request, f"{enrollment.student} enrolled to {enrollment.course.title}"
        )
        return redirect("gradebook:student_detail", pk=pk)
    else:
        return HttpResponseRedirect(reverse(""))


class StatsView(LoginRequiredMixin, TemplateView):
    template_name = "gradebook/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.all()
        enrollments = Enrollment.objects.all()

        grade_level_count = {}
        for student in students:
            if not student.grade_level in grade_level_count:
                grade_level_count[student.grade_level] = 0
            grade_level_count[student.grade_level] += 1

        grade_level_count = dict(sorted(list(grade_level_count.items())))

        grade_stats = [
            (f"{grade}th grade", count) for grade, count in grade_level_count.items()
        ]

        script, div = get_bar_graph(grade_stats)

        final_grade_count = {}
        for enrollment in enrollments:
            if enrollment.final_grade:
                if not enrollment.final_grade in final_grade_count:
                    final_grade_count[enrollment.final_grade] = 0
                final_grade_count[enrollment.final_grade] += 1

        final_grade_count_sorted = dict(
            sorted(list(final_grade_count.items()), key=lambda item: item[0])
        )

        script2, div2 = get_pie_graph(final_grade_count_sorted)

        context["total_students"] = students.count()
        context["grade_levels"] = grade_level_count
        context["show_bokeh"] = True
        context["script"] = script
        context["div"] = div
        context["script2"] = script2
        context["div2"] = div2
        context["total_enrollments"] = enrollments.count()
        context["final_grades"] = final_grade_count_sorted

        return context
