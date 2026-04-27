from django.contrib import admin
from .forms import TeacherCreationForm, TeacherChangeForm
from .models import Teacher
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class TeacherAdmin(UserAdmin):
    """Extend Admin website for custom Teacher model"""

    model = Teacher
    form = TeacherChangeForm
    add_form = TeacherCreationForm
    list_display = [
        "username",
        "email",
        "department",
        "is_staff",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": ("department",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": ("department",),
            },
        ),
    )


admin.site.register(Teacher, TeacherAdmin)
