from flask import render_template, Blueprint
from flask_login import login_required, current_user

from app.models import Course, User, Assignment, Notification
from app.config import db

main_bp = Blueprint("main", __name__, template_folder="templates")


# Home
@main_bp.route("/")
def index():
    users = {"username": "Jonathan"}
    return render_template("main/index.html", users=users)

# Dashboard
@main_bp.route("/dashboard")
@login_required
def dashboard():
    # Notifications (dashboard-only)
    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).order_by(Notification.created_at.desc()).all()

    # Mark notifications as read AFTER displaying them
    for n in notifications:
        n.is_read = True
    db.session.commit()

    # Role-based courses
    if current_user.is_student:
        courses = current_user.get_enrolled_courses()

    elif current_user.is_professor:
        courses = current_user.created_courses  # from backref

    else:  # admin
        courses = Course.query.all()

    return render_template(
        "main/dashboard.html",
        notifications=notifications,
        courses=courses
    )

# Messages
@main_bp.route("/messages")
@login_required
def messages():
    threads = [
        {"id": 1, "from": "Instructor", "subject": "Welcome to the course", "preview": "Let’s have a great semester..."},
        {"id": 2, "from": "TA", "subject": "Assignment reminder", "preview": "Don’t forget Homework 1..."},
    ]
    return render_template("main/messages.html", threads=threads)


@main_bp.route("/messages/<int:msg_id>")
@login_required
def message_detail(msg_id):
    threads = [
        {"id": 1, "from": "Instructor", "subject": "Welcome to the course", "preview": "Let’s have a great semester...", "body": "Welcome! Please read the syllabus and check the schedule."},
        {"id": 2, "from": "TA", "subject": "Assignment reminder", "preview": "Don’t forget Homework 1...", "body": "Homework 1 is due this Friday at 11:59PM."},
    ]

    msg = next((t for t in threads if t["id"] == msg_id), None)
    if not msg:
        flash("Message not found.", "danger")
        return redirect(url_for("main.messages"))

    return render_template("main/message_detail.html", msg=msg)


# GPA calculator
@main_bp.route("/gpa")
@login_required
def gpa_calculator():
    sample_courses = [
        {"name": "CS 146 - Data Structures", "units": 4, "grade": "A"},
        {"name": "CMPE 102 - Assembly Language", "units": 3, "grade": "B+"},
        {"name": "Math 32 - Calculus II", "units": 4, "grade": "A-"},
    ]

    current_gpa = 3.75

    return render_template(
        "main/gpa_calculator.html",
        courses=sample_courses,
        current_gpa=current_gpa
    )


# Assignments (demo page)
@main_bp.route("/courses/<int:course_id>/assignments")
@login_required
def assignments_list(course_id):
    # Fake assignment details for now (replace with Assignment.query later)
    fake_assignments = [
        {"id": 1, "title": "Homework 1", "due_date": "2025-03-10", "points": 100, "status": "Submitted"},
        {"id": 2, "title": "Project Proposal", "due_date": "2025-03-15", "points": 50, "status": "Not submitted"},
    ]

    return render_template(
        "main/assignments_list.html",
        course_id=course_id,
        assignments=fake_assignments
    )
