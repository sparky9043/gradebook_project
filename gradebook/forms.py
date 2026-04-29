from django import forms
from .models import Course


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
        ]
        title = forms.TextInput(
            attrs={"class": "border-2"},
        )
