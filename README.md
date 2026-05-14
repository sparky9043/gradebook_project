# Gradebook

This is my final project that I completed for ComIT course.

## Features

### Authentication & Authorization
- Custom user model (`Teacher`) extending `AbstractUser` via `accounts` app
- JWT-ready authentication setup with `AUTH_USER_MODEL` pointing to custom user
- Login / logout / register views using Django's built-in auth system
- `LoginRequiredMixin` applied to all gradebook views — unauthenticated users redirected to login
- Role-based access control: edit and delete actions gated to `superuser` only
- Permission check at the `dispatch()` level on `StudentEditView` and `StudentDeleteView`
- Edit / delete buttons conditionally rendered in templates — only visible to superusers
- Custom `403 Access Forbidden` page with Material icons and redirect to dashboard
- Custom `404 Page Not Found` page with Material icons and redirect to dashboard

### Courses
- Course list scoped to the logged-in teacher — teachers only see their own courses
- Course detail view showing all enrolled students, sorted alphabetically by last name
- Course creation form
- Pagination on course detail student list (10 per page, manual `Paginator` implementation inside `DetailView`)
- Course statistics view with grade distribution and GPA calculation

### Students
- Student list view with alphabetical ordering by last name
- Pagination on student list (10 per page via `paginate_by`)
- HTMX-powered live search — filters students by first or last name without page reload, returns partial template
- Student detail view showing bio (date of birth, grade level) and all enrolled courses
- Student creation via `<dialog>` modal — no separate page required
- Student edit view only available for `superuser` using `UpdateView` with success message and redirect
- Student delete view only available for `superuser` with confirmation page and success message
- Department-specific material icons on enrolled course cards in student detail
- Add student dialog conditionally shown only on relevant pages via template context

### Enrollments & Grades
- Students enrolled in courses via `Enrollment` through model (M2M with extra fields)
- `unique_together` constraint on `(course, student)` prevents duplicate enrollments
- Enroll student to course from student detail page via modal `<dialog>`
- Teacher authorization check on enrollment — teachers can only enroll students into their own courses
- Grade entry and editing via dedicated `UpdateView` at `/enrollments/<pk>/add-grade/`
- Grade entry restricted to the course's assigned teacher
- Redirect back to student detail page after successful grade update

### Statistics & Visualization
- Per-course grade distribution rendered as a Bokeh pie chart
- Pandas used for data preparation and chart rendering
- GPA calculation with weighted mean across all enrolled students
- Letter grade conversion (A/B/C/D/F ↔ 0–4 scale) via helper functions
- Bokeh CDN scripts conditionally loaded only on pages that use charts
- Helper functions (`get_pie_graph`, `calculate_gpa`, `convert_letter_to_number`, `convert_number_to_letter`) extracted into `helpers.py` — not nested in views

### Design & UI
- Designed with `Stitch with Google`
- Tailwind CSS with custom Material Design 3 color token system defined in `style_tag.html`
- Material Symbols icons throughout (nav, buttons, error pages, course cards)
- Toast notification system — auto-dismisses after 5 seconds, color-coded green/red for success/error
- Sticky header navigation with conditional links based on auth state
- `<dialog>` element used for modals — native HTML, no external library
- Responsive layout with `max-w-7xl` container and gutter spacing
- Partial templates for reusable components (`students_table.html`, `course_detail_students_table.html`, `pagination_buttons.html`, `subject_materials_icon.html`)

### Architecture & Code Quality
- Multi-app structure: `core` (landing), `accounts` (auth), `gradebook` (main features)
- Project settings in `config/` package — clean separation from app code
- `settings.AUTH_USER_MODEL` used for all FK references to the user model
- `SECRET_KEY` loaded from environment variable via `os.getenv()`
- `DEBUG = False` in settings — production-safe
- WhiteNoise middleware for static file serving in production
- `dj-database-url` for database configuration via environment variable
- `render.yaml` and `build.sh` for Render deployment — app is live at `gradebook-project.onrender.com`
- Management command `seed.py` for populating database with test data
- `pyproject.toml` for Python packaging configuration
- `.gitignore` configured

### Tests
- `GradebookTests` covering course creation, student creation, and enrollment creation
- `TeacherManagerTests` covering teacher creation and superuser creation
- All tests use `get_user_model()` — no direct model imports

### Documentation
- `progress.md` — daily development log with dated entries, code snippets, and decision notes covering the full build from April 29 to May 14
- `README.md` present