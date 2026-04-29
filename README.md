# Gradebook

This is my final project that I completed for ComIT course.


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


## To-Do List

[  ] Create `Student` and `Enrollment` models \
[  ] Create `Student` views \
[  ] Add a few students and make enroll them into courses and assign grades