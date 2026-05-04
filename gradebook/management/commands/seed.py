import datetime
import random
from django.core.management.base import BaseCommand
from accounts.models import Teacher
from gradebook.models import Course, Student, Enrollment


class Command(BaseCommand):
    help = "Seeds the database with teachers, courses, students, and enrollments."

    def handle(self, *args, **options):

        # ── Teachers ───────────────────────────────────────────────────────
        # "spark" already exists — get it, don't recreate it
        spark, _ = Teacher.objects.get_or_create(
            username="spark",
            defaults={
                "department": "Math",
                "is_staff": True,
            },
        )

        t_math = spark

        t_science = Teacher.objects.create_user(
            username="tnakamura",
            password="pass1234",
            first_name="Kenji",
            last_name="Nakamura",
            department="Science",
            is_staff=True,
        )
        t_english = Teacher.objects.create_user(
            username="aokafor",
            password="pass1234",
            first_name="Amara",
            last_name="Okafor",
            department="English",
            is_staff=True,
        )
        t_history = Teacher.objects.create_user(
            username="lbertrand",
            password="pass1234",
            first_name="Léa",
            last_name="Bertrand",
            department="History",
            is_staff=True,
        )

        self.stdout.write("  Teachers created.")

        # ── Courses ────────────────────────────────────────────────────────
        # 4 courses per department, assigned to matching teacher

        math_courses = [
            Course.objects.create(title="Algebra I", teacher=t_math),
            Course.objects.create(title="Geometry", teacher=t_math),
            Course.objects.create(title="Pre-Calculus", teacher=t_math),
            Course.objects.create(title="Statistics", teacher=t_math),
        ]
        science_courses = [
            Course.objects.create(title="Biology", teacher=t_science),
            Course.objects.create(title="Chemistry", teacher=t_science),
            Course.objects.create(title="Physics", teacher=t_science),
            Course.objects.create(title="Earth Science", teacher=t_science),
        ]
        english_courses = [
            Course.objects.create(title="English Literature", teacher=t_english),
            Course.objects.create(title="Creative Writing", teacher=t_english),
            Course.objects.create(title="Grammar & Composition", teacher=t_english),
            Course.objects.create(title="Public Speaking", teacher=t_english),
        ]
        history_courses = [
            Course.objects.create(title="World History", teacher=t_history),
            Course.objects.create(title="Canadian History", teacher=t_history),
            Course.objects.create(title="Ancient Civilizations", teacher=t_history),
            Course.objects.create(title="Modern Politics", teacher=t_history),
        ]

        all_courses = math_courses + science_courses + english_courses + history_courses

        self.stdout.write("  Courses created.")

        # ── Students ───────────────────────────────────────────────────────

        first_names = [
            "Aiden",
            "Sofia",
            "Marcus",
            "Yuna",
            "Priya",
            "Ethan",
            "Fatima",
            "Noah",
            "Camille",
            "Jin",
            "Amara",
            "Lucas",
            "Ingrid",
            "Omar",
            "Mei",
            "Liam",
            "Zara",
            "Diego",
            "Hana",
            "Samuel",
            "Nadia",
            "Felix",
            "Aaliya",
            "Tariq",
            "Chloe",
            "Mateus",
            "Seren",
            "Kofi",
            "Elena",
            "Remy",
            "Andrei",
            "Layla",
            "Ivan",
            "Talia",
            "Jace",
            "Nia",
            "Hugo",
            "Simone",
            "Kenji",
            "Astrid",
            "Rafael",
            "Amina",
            "Elias",
            "Yara",
            "Bruno",
            "Chioma",
            "Oscar",
            "Freya",
            "Dante",
            "Mila",
        ]

        last_names = [
            "Tran",
            "Oduya",
            "Svensson",
            "Hassan",
            "Popescu",
            "Ferreira",
            "Al-Rashidi",
            "Kim",
            "Nair",
            "Martin",
            "Chen",
            "Okafor",
            "Nakamura",
            "Bertrand",
            "Patel",
            "Singh",
            "Rivera",
            "Müller",
            "Dubois",
            "Yamamoto",
            "Kowalski",
            "Santos",
            "Andersen",
            "Mensah",
            "Volkov",
            "Diallo",
            "Johansson",
            "Reyes",
            "Nguyen",
            "Fischer",
            "Ivanov",
            "Bakr",
            "Papadopoulos",
            "Nwosu",
            "Eriksson",
            "Hernandez",
            "Lindqvist",
            "Abubakar",
            "Szabo",
            "Tanaka",
            "Cardoso",
            "Petrov",
            "Owusu",
            "Larsson",
            "Moreau",
            "Rashid",
            "Guerrero",
            "Olawale",
            "Bogdanov",
            "Lefevre",
        ]

        students = []
        for i in range(50):
            birth_year = random.randint(2008, 2012)
            birth_month = random.randint(1, 12)
            # Handle varying month lengths simply
            birth_day = random.randint(1, 28)
            dob = datetime.date(birth_year, birth_month, birth_day)

            student = Student.objects.create(
                first_name=first_names[i],
                last_name=last_names[i],
                dob=dob,
                grade_level=random.choice([9, 10, 11, 12]),
            )
            students.append(student)

        self.stdout.write("  Students created.")

        # ── Enrollments ────────────────────────────────────────────────────
        # Each student gets 2–4 courses, randomly chosen from all 16
        # final_grade is randomly assigned
        # date_enrolled is randomised across the last 2 school years

        grade_choices = ["A", "B", "C", "D", "F"]

        # Weighted so F is rare — closer to real grade distribution
        grade_weights = [30, 35, 20, 10, 5]

        enrollment_start = datetime.date(2023, 9, 1)
        enrollment_end = datetime.date(2024, 6, 30)

        def random_date(start, end):
            delta = (end - start).days
            return start + datetime.timedelta(days=random.randint(0, delta))

        for student in students:
            num_courses = random.randint(2, 4)
            chosen_courses = random.sample(all_courses, num_courses)

            for course in chosen_courses:
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    final_grade=random.choices(
                        grade_choices, weights=grade_weights, k=1
                    )[0],
                    # Override auto_now_add by using a workaround below
                )

        self.stdout.write("  Enrollments created.")
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
