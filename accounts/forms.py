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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "w-full pl-12 pr-5 py-3.5 bg-surface-container-low border border-outline-variant/15 rounded-lg focus:outline-none focus:ring-4 focus:ring-primary-fixed focus:border-primary transition-all font-body text-sm text-on-surface placeholder:text-outline-variant",
            },
        )
        self.fields["password1"].widget.attrs.update(
            {
                "class": "w-full pl-12 pr-5 py-3.5 bg-surface-container-low border border-outline-variant/15 rounded-lg focus:outline-none focus:ring-4 focus:ring-primary-fixed focus:border-primary transition-all font-body text-sm text-on-surface",
                "placeholder": "••••••••",
            },
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "w-full pl-12 pr-5 py-3.5 bg-surface-container-low border border-outline-variant/15 rounded-lg focus:outline-none focus:ring-4 focus:ring-primary-fixed focus:border-primary transition-all font-body text-sm text-on-surface",
                "placeholder": "••••••••",
            },
        )
        self.fields["department"].widget.attrs.update(
            {
                "class": "w-full pl-12 pr-10 py-3.5 bg-surface-container-low border border-outline-variant/15 rounded-lg focus:outline-none focus:ring-4 focus:ring-primary-fixed focus:border-primary transition-all font-body text-sm text-on-surface appearance-none",
            }
        )


class TeacherChangeForm(UserChangeForm):
    """Form used to edit Teacher Admin"""

    class Meta:
        model = Teacher
        fields = UserChangeForm.Meta.fields


class TeacherLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        input_style = "w-full bg-surface-container-low border border-outline-variant/15 rounded-lg px-5 py-4 text-on-surface placeholder:text-outline focus:ring-4 focus:ring-primary-fixed focus:border-primary transition-all outline-none"

        self.fields["username"].widget.attrs.update(
            {
                "class": input_style,
                "autocomplete": "username",
                "placeholder": "Enter Username",
            },
        )
        self.fields["password"].widget.attrs.update(
            {
                "class": input_style,
                "placeholder": "••••••••",
            },
        )
        # self.fields["username"].widget = forms.TextInput(
        # attrs={
        #     "class": input_style,
        #     "autocomplete": "username",
        #     "placeholder": "Enter Username",
        # },
        # )
        # self.fields["password"].widget = forms.PasswordInput(
        # attrs={
        #     "class": input_style,
        #     "placeholder": "••••••••",
        # },
        # )
