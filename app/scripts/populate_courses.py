import random

from app import create_app
from app.config import db
from app.models import User, Course, Enrollment

def populate_courses():
    # Each entry has course fields & a professor email that links to that professor's User
    courses_data = [
        {
            "course": {
                "code": "PHYS51",
                "title": "General Physics II",
                "description": (
                    "A calculus-based introduction to electricity and magnetism, "
                    "covering electric charges, electric and magnetic fields, "
                    "dc and ac circuits, and electromagnetic waves."
                ),
                "credits": 4,
                "professor": "John Doe",
                "availability": True,
                "format": "online",
                "max_students": 30,
            },
            "professor_email": "john.doe@university.edu",
        },
        {
            "course": {
                "code": "CMPE131",
                "title": "Software Engineering I",
                "description": (
                    "Why software engineering? What is software engineering? "
                    "Software development lifecycle activities: project planning "
                    "and management requirements analysis, requirement specification. "
                    "Software design, software testing, verification, validation, "
                    "and documentation. Software quality assurance and review "
                    "techniques, software maintenance, team-based projects."
                ),
                "credits": 3,
                "professor": "Carlos Rojas",
                "availability": True,
                "format": "in-person",
                "max_students": 25,
            },
            "professor_email": "carlos.rojas@university.edu",
        },
        {
            "course": {
                "code": "CMPE102",
                "title": "Assembly Language Programming",
                "description": (
                    "Assembly programming; assembly-C interface; CPU and memory "
                    "organization; addressing modes; arithmetic, logic and branch "
                    "instructions; arrays, pointers, subroutines, stack and procedure "
                    "calls; software interrupts; multiplication, division and "
                    "floating point arithmetic."
                ),
                "credits": 3,
                "professor": "Michael Green",
                "availability": True,
                "format": "in-person",
                "max_students": 20,
            },
            "professor_email": "michael.green@university.edu",
        },
        {
            "course": {
                "code": "ISE130",
                "title": "Engineering Probability and Statistics",
                "description": (
                    "Probability theory, graphical displays of data, graphical "
                    "methods of comparisons of samples and hypotheses testing. "
                    "Statistical estimation and inference. Uses graphical "
                    "statistical packages."
                ),
                "credits": 3,
                "professor": "Emily Samson",
                "availability": True,
                "format": "in-person",
                "max_students": 28,
            },
            "professor_email": "emily.aamson@university.edu",
        },
        {
            "course": {
                "code": "ENGR10",
                "title": "Introduction to Engineering",
                "description": (
                    "Introduction to engineering through hands-on design projects, "
                    "case studies, and problem-solving using computers. Students "
                    "also acquire non-technical skills, such as team skills and "
                    "the ability to deal with ethical dilemmas."
                ),
                "credits": 3,
                "professor": "David Bee",
                "availability": True,
                "format": "online",
                "max_students": 40,
            },
            "professor_email": "david.bee@university.edu",
        },
        {
            "course": {
                "code": "CS49J",
                "title": "Programming in Java",
                "description": (
                    "Introduction to the Java programming language and libraries. "
                    "Topics include fundamental data types and control structures, "
                    "object-oriented programming, string processing, input/output, "
                    "and error handling. Use of Java libraries for mathematics, "
                    "graphics, collections, and for user interfaces."
                ),
                "credits": 3,
                "professor": "Taylor Dave",
                "availability": False,
                "format": "online",
                "max_students": 35,
            },
            "professor_email": "taylor.dave@university.edu",
        },
    ]

    app = create_app()

    with app.app_context():

        # Fill the database with up to 20 students
        existing_students = User.query.filter_by(role=User.ROLE_STUDENT).count()
        to_create = max(0, 20 - existing_students)

        for i in range(existing_students + 1, existing_students + 1 + to_create):
            email = f"student_{i}@university.edu"
            student = User(
                email=email,
                avatar_url=f"https://ui-avatars.com/api/?name=Student+{i}",
                role=User.ROLE_STUDENT,
            )
            student.set_password("password123")
            db.session.add(student)

        if to_create > 0:
            db.session.commit()
            print(f"{to_create} student accounts created.")
        else:
            print("Already have over 20 students. Skipping student creation.")

        # Create courses and link to professor users by email
        if Course.query.count() == 0:
            for entry in courses_data:
                course_data = entry["course"]
                prof_email = entry["professor_email"]

                course = Course(**course_data)

                professor_user = User.query.filter_by(email=prof_email).first()
                if professor_user:
                    course.professor_user = professor_user
                else:
                    print(
                        f"WARNING: No professor user with email {prof_email} "
                        f"for course {course_data['code']}"
                    )

                db.session.add(course)

            db.session.commit()
            print(f"{len(courses_data)} courses created.")
        else:
            print("Courses already exist. Skipping course creation.")

        # Randomly enroll each student in 2–5 available courses
        courses = Course.query.filter_by(availability=True).all()
        students = User.query.filter_by(role=User.ROLE_STUDENT).all()

        total_enrollments = 0

        for student in students:
            num_courses = random.randint(2, 5)
            selected_courses = random.sample(courses, num_courses)

            for course in selected_courses:
                # avoid duplicates due to UniqueConstraint
                if not Enrollment.query.filter_by(
                    user_id=student.id, course_id=course.id
                ).first():
                    enrollment = Enrollment(
                        user_id=student.id,
                        course_id=course.id,
                    )
                    db.session.add(enrollment)
                    total_enrollments += 1

        db.session.commit()
        print(f"Random enrollment complete. {total_enrollments} enrollments added.")

if __name__ == "__main__":
    populate_courses()
