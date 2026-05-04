from django.db import models
from django.conf import settings


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
    )

    def __str__(self):
        return self.title


class Student(models.Model):
    GRADE_LEVEL_CHOICES = [
        (9, "Grade 9"),
        (10, "Grade 10"),
        (11, "Grade 11"),
        (12, "Grade 12"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    grade_level = models.IntegerField(choices=GRADE_LEVEL_CHOICES)
    courses = models.ManyToManyField(
        Course,
        through="Enrollment",
        related_name="students",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    GRADE_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("F", "F"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )

    final_grade = models.CharField(
        max_length=1,
        choices=GRADE_CHOICES,
        blank=True,
        default="",
    )

    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "student")
        ordering = ["course__title"]

    def __str__(self):
        return f"[{self.course}] {self.student} Final Grade: {self.final_grade}"
