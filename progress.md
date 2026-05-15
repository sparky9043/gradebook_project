# Project Progress

## To-Do List

[ x ] Create `Student` and `Enrollment` models \
[ x ] Add a few students and make enroll them into courses and assign grades \
[ x ] Create `Student` views \
[ x ] Create toast message \
[ x ] Use `<dialog>` for creating student \
[ x ] Show each student detail when clicking student name \
[ x ] Create `Enrollment` form and views \
[ x ] Create `gradebook/enrollments/<int:pk>/add-grade/` route \
[ x ] Consider using 'context' to include dialog in the base.html when entering certain views \
     (i.e. dialog should only appear when in Students list page and Student details page)
[ x ] Add an `Enroll Class` button inside `StudentDetailView` \
[ x ] Add `SearchView` using `HTMX` in the `StudentsListView` \
[ x ] Consider adding pagination in List View \
[ x ] Consider adding pagination in Detail View \

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

### 5/11/2026
  1. Create `SearchView` for students list powered by `HTMX`
    a. Use `HTMX` to send request to `students/search` view and return `templates/gradebook/partials/students_table.html` in `StudentsListView`
  2. Change `bokeh` bar graph to circle graph
  3. Install `pandas` among other packages to change bar graph to circle graph
  4. Add `gradebook/enrollments/<int:pk>/add-grade` page to add or edit student final grade -> redirect to `gradebook:student_detail` upon success
  5. Allow teacher to edit student final grade only for students in their own course
  6. Prevent other teachers from entering grades for students not in their course

### 5/12/2026
  1. Add pagination using `paginate_by` in `ListView` and catching in templates with `page_obj` and `paginator`
  2. Learned how to and employed pagination in `DetailView`
    a. First use `get_context_data` to get list
    b. `from django.core.paginator import Paginator`
    c. Pass the fetched data into `Paginator(data, number)` and replace number with how many you want per page
    d. use `context['page_obj']` and `context['paginator']` to manually pass the page_obj and paginator
  3. Use Stitch to add styles to pagination buttons
  4. Refactor tables and pagination buttons into their own `html` files
  5. Correctly use `paginator.object_list.count` to get total number of students in students list
  6. Add an actions column in students list


### 5/13/2026
  1. Add `StudentEditView` by reusing `StudentCreationForm` in `gradebook/forms.py` and extending `UpdateView` class
  2. Add cancel button that redirects user to students list
  3. Make `StudentEditView` display success messages when user edits student and redirect back to list
  4. Add `StudentDeleteView` for confirming if teacher wants to delete user
  5. Add delete materials button in `student_detail.html` for easy access to delete page


### 5/14/2026
  1. Add customized `403.html` and `404.html` pages
  2. Redirect user to `403.html` if the user is not `superuser` and they try to edit or delete student
  3. Show edit and delete buttons only to `superuser`


### 5/15/2026
  1. Add `Stats` page to `gradebook/stats` url path
  2. Display grade level distribution and final grade distribution in stats page