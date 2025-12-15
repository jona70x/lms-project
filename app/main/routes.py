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
    all_courses = Course.query.all()

    notifications = [
        {"message": "You haven’t checked Week 3 notes."},
        {"message": "New message in CMPE 102 discussion board."}
    ]

    return render_template(
        "main/dashboard.html",
        courses=all_courses,
        notifications=notifications
    )

# Messages
@main_bp.route("/messages")
@login_required
def messages():
    return render_template("main/messages.html")


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
