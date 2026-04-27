from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.


# DON'T FORGET TO USE LOCAL DB BEFORE TESTING
class TeacherManagerTests(TestCase):
    def test_create_teacher(self):
        User = get_user_model()
        new_user = User.objects.create_user(
            username="testuser",
            password="testuser1234",
            email="testuser@example.com",
        )

        self.assertEqual(new_user.username, "testuser")
        self.assertEqual(new_user.email, "testuser@example.com")
