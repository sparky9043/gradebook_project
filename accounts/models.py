from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Teacher(AbstractUser):
    """Represents admin as Teacher

    Attributes:
        is_staff (bool): Determines whether Teacher is staff; True by default
        department (str): Department that teacher belongs to using choices
    """

    is_staff = models.BooleanField(default=True)
    department = models.CharField(
        max_length=50,
        choices=[
            ("Math", "Math"),
            ("Science", "Science"),
            ("English", "English"),
            ("History", "History"),
        ],
    )
