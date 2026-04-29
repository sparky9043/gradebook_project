from django import forms
from .models import Course


class CourseCreationForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            "title",
            "teacher",
        ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["title"].widget.attrs.update({"class": "border-2 "})
