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
