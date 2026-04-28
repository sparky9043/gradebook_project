from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)
from .models import Teacher
from django import forms


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


class TeacherLoginForm(AuthenticationForm):
    class Meta:
        model = Teacher

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = forms.TextInput(
            attrs={
                "class": "w-full bg-surface-container-low border border-outline-variant/15 rounded-lg px-5 py-4 text-on-surface placeholder:text-outline focus:ring-4 focus:ring-primary-fixed focus:border-primary transition-all outline-none",
                "autocomplete": "username",
            },
        )
        self.fields["password"].widget = forms.PasswordInput(
            attrs={
                "class": "w-full bg-surface-container-low border border-outline-variant/15 rounded-lg px-5 py-4 text-on-surface placeholder:text-outline focus:ring-4 focus:ring-primary-fixed focus:border-primary transition-all outline-none",
            },
        )
