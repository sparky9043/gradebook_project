from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Teacher


class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = UserCreationForm.Meta.fields + ("department",)


class TeacherChangeForm(UserChangeForm):
    class Meta:
        model = Teacher
        fields = UserChangeForm.Meta.fields
