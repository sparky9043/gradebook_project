from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Teacher


class TeacherCreationForm(UserCreationForm):
    """Form used to create Teacher Admin"""

    class Meta:
        model = Teacher
        fields = UserCreationForm.Meta.fields + ("department",)


class TeacherChangeForm(UserChangeForm):
    """Form used to edit Teacher Admin"""

    class Meta:
        model = Teacher
        fields = UserChangeForm.Meta.fields
