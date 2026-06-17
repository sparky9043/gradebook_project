# Gradebook

A full-stack Django web application for high school teachers to manage courses, students, enrollments, and grades. Built with role-based access control, live search, and interactive data visualization.

---

## Links

Live Version: `https://gradebook-project.onrender.com/`
GitHub Repo: `https://github.com/sparky9043/gradebook_project/`

## Features

### Authentication
- Custom `Teacher` model extending Django's `AbstractUser`
- Register, login, and logout
- All views protected with `LoginRequiredMixin`

### Role-Based Access Control
Two tiers enforced at the `dispatch()` level — not just in templates:

| Action | Regular Teacher | Superuser |
|---|---|---|
| View own courses | ✅ | ✅ |
| View all courses | ❌ | ✅ |
| Create course | ✅ | ✅ |
| Delete course | ❌ | ✅ |
| Add students | ✅ | ✅ |
| Edit students | ❌ | ✅ |
| Delete students | ❌ | ✅ |
| Enroll students | ✅ (own courses only) | ✅ |
| Record grades | ✅ (own courses only) | ✅ |
| School-wide stats | ❌ | ✅ |

### Course Management
- Create and list courses (scoped to the logged-in teacher)
- Course detail view with enrolled students, sorted alphabetically
- Paginated student table (10 per page)
- Course statistics: grade distribution pie chart + class GPA

### Student Management
- Add students via modal dialog (no page redirect)
- Edit and delete student records (superuser only)
- HTMX-powered live search — filters by first or last name without a page reload
- Paginated student list (10 per page)

### Enrollment & Grades
- Enroll students into courses from the student detail page
- Teachers can only enroll into their own courses
- Record final grades (A / B / C / D / F) per enrollment
- Enrollment protected against duplicates via `unique_together`

### Analytics & Visualization
- **Course Stats:** interactive Bokeh pie chart showing grade distribution + GPA calculation
- **School Stats:** bar chart showing student count by grade level (9–12)
- GPA computed using a weighted mean across all enrolled students
- Helper functions (`calculate_gpa`, `convert_letter_to_number`, `convert_number_to_letter`) live in `gradebook/helpers.py`
- Bokeh CDN scripts load conditionally — only on pages that render charts

### UI & UX
- Material Design 3 color token system via custom Tailwind CSS config
- Toast notifications (success / error) with 5-second auto-dismiss
- Custom `403 Access Forbidden` and `404 Not Found` error pages
- Sticky navigation with auth-conditional links
- Native HTML `<dialog>` element for modals — no external library required
- Responsive layout with `max-w-7xl` container

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13+ |
| Framework | Django 6.x |
| Database (dev) | SQLite |
| Database (prod) | PostgreSQL via `dj-database-url` |
| Charts | Bokeh |
| Data processing | Pandas |
| Dynamic UI | HTMX |
| Styling | Tailwind CSS + Material Design 3 tokens |
| Static files | WhiteNoise |
| Deployment | Render |

---

## Project Structure

```
├── config/               # Project settings, root URLs, WSGI/ASGI
├── core/                 # Landing page and home views
├── accounts/             # Custom Teacher model, auth views (login/register/logout)
├── gradebook/            # Courses, students, enrollments, stats
│   ├── helpers.py        # GPA and grade conversion utilities
│   ├── models.py         # Course, Student, Enrollment
│   ├── views.py          # CBVs + FBVs for all gradebook features
│   └── management/
│       └── commands/
│           └── seed.py   # Database seeding command
├── templates/            # Project-level base, nav, error pages
└── static/               # JavaScript (HTMX interactions, toast dismiss)
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sparky9043/gradebook.git
cd gradebook
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
```

To generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

For production, also add:

```env
DATABASE_URL=postgres://user:password@host:5432/dbname
DEBUG=False
ALLOWED_HOSTS=your-domain.com
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

The superuser account has full access to all features including student editing, deletion, and school-wide statistics.

---

## Loading Seed Data

The project includes a management command that wipes existing data and populates the database with:

- **4 teachers** (one per department: Math, Science, English, History)
- **16 courses** (4 per teacher)
- **200 students** (unique names, random grade levels 9–12, DOBs 2008–2012)
- **~800–1,200 enrollments** (4–7 courses per student, weighted grade distribution)

Run the seed command:

```bash
python manage.py seed
```

Output confirms counts and verifies constraints:

```
  Wiping existing data...
  All tables cleared.
  4 teachers created.
  18 courses created.
  200 students created.
  1,043 enrollments created.
  Students per course — min: 45, max: 72
  Courses per student — min: 4, max: 7
  Database seeded successfully!
```

> **Note:** The seed command deletes all existing teachers, courses, students, and enrollments before inserting fresh data. To preserve a specific superuser account, the seed does not delete users in the `auth_user` table directly — only `Teacher` records created by previous seeds are removed.

To reseed from scratch at any time:

```bash
python manage.py seed
```

---

## Running the Development Server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

Log in with the superuser account you created, or use one of the seeded teacher accounts:

| Username | Password | Department |
|---|---|---|
| `spark` | `password123` | Math |
| `tnakamura` | `password123` | Science |
| `aokafor` | `password123` | English |
| `lbertrand` | `password123` | History |

---

## Running Tests

```bash
python manage.py test
```

Tests cover model creation for `Teacher`, `Course`, `Student`, and `Enrollment`.

---

## Deployment (Render)

The project is configured for one-click deployment on Render using `render.yaml` and `build.sh`.

The `build.sh` script runs automatically on deploy:

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Required environment variables on Render:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | PostgreSQL connection string (auto-set by Render) |
| `DEBUG` | Set to `False` in production |

---

For detailed information on how to deploy on Render, visit `https://render.com/`
