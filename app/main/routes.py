from flask import render_template, Blueprint, request
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


from flask import render_template, Blueprint, request
from flask_login import login_required, current_user

from app.models import Course, User, Assignment, Notification
from app.config import db

# ...

@main_bp.route("/gpa", methods=["GET", "POST"])
@login_required
def gpa_calculator():
    grade_scale = {
        "A": 4.0, "A-": 3.7,
        "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7,
        "D+": 1.3, "D": 1.0,
        "F": 0.0,
    }

    current_gpa = None

    if request.method == "GET":
        # pull courses from DB for this user
        db_courses = current_user.get_enrolled_courses() 
        courses = [
            {
                "name": f"{c.code} - {c.title}",
                "units": c.credits,
                "grade": "",  # TODO dynamically update with current grade
            }
            for c in db_courses
        ]

    else:  # POST
        course_names = request.form.getlist("course_name")
        units_list   = request.form.getlist("units")
        grades       = request.form.getlist("grade")

        total_points = 0.0
        total_units  = 0.0
        courses      = []

        for name, u, g in zip(course_names, units_list, grades):
            if not name:
                continue

            try:
                units = float(u) if u else 0.0
            except ValueError:
                units = 0.0

            courses.append({
                "name": name,
                "units": units,
                "grade": g,
            })

            if not g or units <= 0:
                continue

            total_units  += units
            total_points += grade_scale.get(g, 0.0) * units

        if total_units > 0:
            current_gpa = round(total_points / total_units, 2)

    return render_template(
        "main/gpa_calculator.html",
        courses=courses,
        current_gpa=current_gpa,
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
