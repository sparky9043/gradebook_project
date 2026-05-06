from django.test import TestCase
from .models import Student, Course
from datetime import date
from django.contrib.auth import get_user_model


# Create your tests here.
class GradebookTests(TestCase):
    """Test for Gradebook App"""

    def test_create_course(self):
        Teacher = get_user_model()
        teacher = Teacher.objects.create_user(
            username="testuser",
            password="testuser1234",
            email="testuser@example.com",
        )

        course = Course.objects.create(
            title="Introduction to Philosophy",
            teacher=teacher,
        )

        self.assertEqual(course.title, "Introduction to Philosophy")
        self.assertEqual(course.teacher.username, "testuser")

    def test_create_student(self):
        student = Student.objects.create(
            first_name="Jimmy",
            last_name="Hendrix",
            dob=date(2011, 10, 13),
            grade_level=10,
        )

        self.assertEqual(student.first_name, "Jimmy")
        self.assertEqual(student.last_name, "Hendrix")
        self.assertEqual(student.dob.year, 2011)
