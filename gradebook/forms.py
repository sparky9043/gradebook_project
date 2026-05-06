from django import forms
from .models import Course, Student


class CourseCreationForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            "title",
            "teacher",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {
                "class": "w-full bg-surface-container-low border-outline-variant border-opacity-15 rounded-lg px-5 py-4 focus:ring-4 focus:ring-primary-fixed focus:border-primary transition-all duration-300 font-body text-lg outline-none placeholder:text-outline/40",
                "placeholder": "e.g. The Ethics of Ancient Philosophy",
            }
        )


class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name",
            "last_name",
            "dob",
            "grade_level",
        ]
