import datetime
import random
from django.core.management.base import BaseCommand
from accounts.models import Teacher
from gradebook.models import Course, Student, Enrollment


class Command(BaseCommand):
    help = "Wipes all data and reseeds with 4 teachers, 18 courses, 200 students, and enrollments."

    def handle(self, *args, **options):

        # ── Wipe ALL existing data ─────────────────────────────────────────
        # Order matters: delete dependents before parents to avoid FK errors.
        self.stdout.write("  Wiping existing data...")
        Enrollment.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.all().delete()
        Teacher.objects.all().delete()
        self.stdout.write("  All tables cleared.")

        # ── Teachers ───────────────────────────────────────────────────────
        t_math = Teacher.objects.create_user(
            username="spark",
            password="password123",
            first_name="Steve",
            last_name="Park",
            department="Math",
            is_staff=True,
        )
        t_science = Teacher.objects.create_user(
            username="tnakamura",
            password="password123",
            first_name="Kenji",
            last_name="Nakamura",
            department="Science",
            is_staff=True,
        )
        t_english = Teacher.objects.create_user(
            username="aokafor",
            password="password123",
            first_name="Amara",
            last_name="Okafor",
            department="English",
            is_staff=True,
        )
        t_history = Teacher.objects.create_user(
            username="lbertrand",
            password="password123",
            first_name="Lea",
            last_name="Bertrand",
            department="History",
            is_staff=True,
        )
        self.stdout.write("  4 teachers created.")

        # ── Courses ────────────────────────────────────────────────────────
        # Math: 5 courses | Science: 4 | English: 5 | History: 4 → 18 total

        math_courses = [
            Course.objects.create(title="Algebra I", teacher=t_math),
            Course.objects.create(title="Geometry", teacher=t_math),
            Course.objects.create(title="Pre-Calculus", teacher=t_math),
            Course.objects.create(title="Statistics", teacher=t_math),
            Course.objects.create(title="Calculus AB", teacher=t_math),
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
            Course.objects.create(title="Media & Rhetoric", teacher=t_english),
        ]
        history_courses = [
            Course.objects.create(title="World History", teacher=t_history),
            Course.objects.create(title="Canadian History", teacher=t_history),
            Course.objects.create(title="Ancient Civilizations", teacher=t_history),
            Course.objects.create(title="Modern Politics", teacher=t_history),
        ]

        all_courses = math_courses + science_courses + english_courses + history_courses
        # Build a lookup dict so we can find Course objects by pk quickly later
        course_by_pk = {c.pk: c for c in all_courses}

        self.stdout.write(f"  {len(all_courses)} courses created.")

        # ── Students ───────────────────────────────────────────────────────
        # 200 unique first names — no duplicates in this list.
        first_names = [
            # 1–10
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
            # 11–20
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
            # 21–30
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
            # 31–40
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
            # 41–50
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
            # 51–60
            "Adrian",
            "Nora",
            "Cyrus",
            "Leila",
            "Xavier",
            "Amelia",
            "Rohan",
            "Iris",
            "Tobias",
            "Sana",
            # 61–70
            "Kieran",
            "Zoe",
            "Emre",
            "Petra",
            "Kwame",
            "Vivian",
            "Darius",
            "Sakura",
            "Brennan",
            "Asha",
            # 71–80
            "Nikolai",
            "Celia",
            "Hamza",
            "Miriam",
            "Jonas",
            "Kaito",
            "Serena",
            "Emeka",
            "Luna",
            "Bastian",
            # 81–90
            "Ayaan",
            "Fiona",
            "Callum",
            "Yasmin",
            "Leo",
            "Naomi",
            "Matteo",
            "Ines",
            "Tristan",
            "Zainab",
            # 91–100
            "Finn",
            "Adaeze",
            "Beckett",
            "Kira",
            "Soren",
            "Thalia",
            "Idris",
            "Vesna",
            "Ezra",
            "Nkechi",
            # 101–110
            "Jonah",
            "Elara",
            "Riku",
            "Anika",
            "Luca",
            "Dahlia",
            "Alaric",
            "Yuki",
            "Griffin",
            "Pita",
            # 111–120
            "Celeste",
            "Ren",
            "Aoife",
            "Femi",
            "Zaynab",
            "Casimir",
            "Linh",
            "Stellan",
            "Aditi",
            "Cian",
            # 121–130
            "Mirabel",
            "Zander",
            "Chidinma",
            "Leander",
            "Sage",
            "Ilya",
            "Kameko",
            "Dorian",
            "Zahra",
            "Emilian",
            # 131–140
            "Tova",
            "Seun",
            "Reverie",
            "Caspian",
            "Nour",
            "Aleksei",
            "Tamsin",
            "Orion",
            "Safiya",
            "Benicio",
            # 141–150
            "Isadora",
            "Caden",
            "Feya",
            "Sylvester",
            "Ximena",
            "Caelum",
            "Amahle",
            "Finnian",
            "Devika",
            "Gideon",
            # 151–160
            "Ysolde",
            "Emiliano",
            "Nneka",
            "Theron",
            "Calliope",
            "Lysander",
            "Fumiko",
            "Kenzo",
            "Naira",
            "Evander",
            # 161–170
            "Tessaly",
            "Makena",
            "Ozzy",
            "Isola",
            "Brennius",
            "Leilani",
            "Ike",
            "Sorcha",
            "Phelan",
            "Amaris",
            # 171–180
            "Idowu",
            "Celestine",
            "Riordan",
            "Ozlem",
            "Evren",
            "Talitha",
            "Osiris",
            "Yemisi",
            "Cadmus",
            "Zephyrine",
            # 181–190
            "Bodhi",
            "Sienna",
            "Kazimir",
            "Elowen",
            "Thaddeus",
            "Zuri",
            "Sable",
            "Alistair",
            "Paloma",
            "Caelan",
            # 191–200
            "Abiodun",
            "Vesper",
            "Percival",
            "Ottilie",
            "Oluwatobi",
            "Lyra",
            "Cormac",
            "Adaora",
            "Waverly",
            "Isolde",
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
            "Muller",
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
            "Nakagawa",
            "Osei",
            "Kovalenko",
            "Mbeki",
            "Vasquez",
            "Sorensen",
            "Adeyemi",
            "Kovacs",
            "Wangari",
            "Fernandes",
            "Obinna",
            "Gupta",
            "Thornton",
            "Miyamoto",
            "Nzinga",
            "Beaumont",
            "Achebe",
            "Lindgren",
            "Khoury",
            "Farouk",
            "Okonkwo",
            "Peralta",
            "Stefanidis",
            "Nyambura",
            "Boateng",
            "Hashimoto",
            "Tremblay",
            "Oyelaran",
            "Magnusson",
            "Salazar",
            "Zuberi",
            "Delacroix",
            "Ndiaye",
            "Kobayashi",
            "Olofsson",
            "Eze",
            "Dupont",
            "Kariuki",
            "Maier",
            "Souza",
            "Abramov",
            "Solberg",
            "Kamara",
            "Pires",
            "Otieno",
            "Henriksen",
            "Lopes",
            "Dlamini",
            "Girard",
            "Okeke",
        ]

        # Each student uses first_names[i] (guaranteed unique) + random last name
        students = []
        for i in range(200):
            birth_year = random.randint(2008, 2012)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)  # capped at 28 — always valid
            student = Student.objects.create(
                first_name=first_names[i],
                last_name=random.choice(last_names),
                dob=datetime.date(birth_year, birth_month, birth_day),
                grade_level=random.choice([9, 10, 11, 12]),
            )
            students.append(student)

        self.stdout.write(f"  {len(students)} students created.")

        # ── Enrollment allocation ──────────────────────────────────────────
        # Rules:
        #   • Every course must have ≥ 15 students
        #   • Every student must have 4–7 courses
        #   • Every enrollment must have a non-empty final_grade
        #   • No duplicate (student, course) pairs

        grade_choices = ["A", "B", "C", "D", "F"]
        grade_weights = [30, 35, 20, 10, 5]  # weighted: A/B most common, F rare

        # Track allocations as sets of pks to make membership checks O(1)
        student_to_courses = {
            s.pk: set() for s in students
        }  # student_pk → {course_pks}
        course_to_students = {
            c.pk: set() for c in all_courses
        }  # course_pk  → {student_pks}

        # ── Phase 1: guarantee every course has ≥ 15 students ─────────────
        for course in all_courses:
            pool = [s for s in students if course.pk not in student_to_courses[s.pk]]
            selected = random.sample(pool, min(15, len(pool)))
            for s in selected:
                student_to_courses[s.pk].add(course.pk)
                course_to_students[course.pk].add(s.pk)

        # ── Phase 2: guarantee every student has ≥ 4 courses ──────────────
        for student in students:
            shortfall = 4 - len(student_to_courses[student.pk])
            if shortfall > 0:
                available = [
                    c for c in all_courses if c.pk not in student_to_courses[student.pk]
                ]
                for course in random.sample(available, min(shortfall, len(available))):
                    student_to_courses[student.pk].add(course.pk)
                    course_to_students[course.pk].add(student.pk)

        # ── Phase 3: randomly top up to 7 courses per student ─────────────
        for student in students:
            headroom = 7 - len(student_to_courses[student.pk])
            if headroom > 0:
                available = [
                    c for c in all_courses if c.pk not in student_to_courses[student.pk]
                ]
                if available:
                    extras = random.sample(
                        available, random.randint(0, min(headroom, len(available)))
                    )
                    for course in extras:
                        student_to_courses[student.pk].add(course.pk)
                        course_to_students[course.pk].add(student.pk)

        # ── Phase 4: bulk-create all Enrollment rows ───────────────────────
        enrollments = []
        for student in students:
            for course_pk in student_to_courses[student.pk]:
                enrollments.append(
                    Enrollment(
                        student=student,
                        course=course_by_pk[course_pk],
                        final_grade=random.choices(
                            grade_choices, weights=grade_weights, k=1
                        )[0],
                    )
                )

        Enrollment.objects.bulk_create(enrollments)
        self.stdout.write(f"  {len(enrollments)} enrollments created.")

        # ── Verification summary ───────────────────────────────────────────
        min_per_course = min(len(v) for v in course_to_students.values())
        max_per_course = max(len(v) for v in course_to_students.values())
        min_per_student = min(len(v) for v in student_to_courses.values())
        max_per_student = max(len(v) for v in student_to_courses.values())

        self.stdout.write(
            f"  Students per course  — min: {min_per_course},  max: {max_per_course}"
        )
        self.stdout.write(
            f"  Courses per student  — min: {min_per_student}, max: {max_per_student}"
        )
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
