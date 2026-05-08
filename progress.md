## Project Progress

### 4/29/2026
  1. Start `gradebook` app
  2. Create `Course` model
```python
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
```
  3. Create `gradebook/` `gradebook/courses/` `gradebook/courses/<int:pk>/` url paths and views + templates for each 


### 5/4/2026
  1. Create `Student` and `Enrollment` models
   ```python
    class Student(models.Model):
        GRADE_LEVEL_CHOICES = [
            (9, "Grade 9"),
            (10, "Grade 10"),
            (11, "Grade 11"),
            (12, "Grade 12"),
        ]

        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        dob = models.DateField()
        grade_level = models.IntegerField(choices=GRADE_LEVEL_CHOICES)
        courses = models.ManyToManyField(
            Course,
            through="Enrollment",
            related_name="students",
        )

        def __str__(self):
            return f"{self.first_name} {self.last_name}"


    class Enrollment(models.Model):
        GRADE_CHOICES = [
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("F", "F"),
        ]

        course = models.ForeignKey(
            Course,
            on_delete=models.CASCADE,
            related_name="enrollments",
        )

        student = models.ForeignKey(
            Student,
            on_delete=models.CASCADE,
            related_name="enrollments",
        )

        final_grade = models.CharField(
            max_length=1,
            choices=GRADE_CHOICES,
            blank=True,
            default="",
        )

        date_enrolled = models.DateField(auto_now_add=True)

        class Meta:
            unique_together = ("course", "student")
            ordering = ["course__title"]

        def __str__(self):
            return f"[{self.course}] {self.student} Final Grade: {self.final_grade}"

   ```
  2. Create `gradebook/management/commands/seed.py` for populating data with base data
  3. Tested the app locally before deploying on `[Render](https://gradebook-project.onrender.com/)`

### 5/5/2026
  1. Make `students/` path display list of students
  2. Use `DetailView` to show `students/<int:pk>/` details for each student
  3. Major style upgrade

### 5/6/2026
  1. Make `students/<int:pk>/` path display student details
  2. Show student bio (i.e. dob) and enrolled courses
  3. Make each enrolled course show different materials icon by department
  4. Use `<dialog>` element for creating new students
  5. Add `static/js/addStudentDialog.js` and `static/js/toastMessage.js` files for adding event listeners and timeouts for toast and show dialog buttons
  6. Make each toast message show either red or green icons for success or error messages, respectively

### 5/7/2026
  1. Add `students/<int:pk>/enroll` path and show forms for enrolling student to course
  2. Used FBV to `create enroll_student_view`
  3. Used custom template `gradebook/enrollment.html` for enrolling student
  4. Refactored JS code into a single `static/js/script.js` file
  5. Fix error displayed in the console when the js file tried to attach an event listener to a null element

### 5/8/2026
  1. Create a `gradebook/courses/<int:pk>/stats` url and show basic stats per course
  2. Install `bokeh` package to convert grade distribution to bar graph
  3. Add material icons to `Login`, `Logout`, and `Add Student` buttons for cleaner UI 
