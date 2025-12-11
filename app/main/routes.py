from flask import render_template, Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.decorators import roles_required
from app.models import Course, User, Assignment
from app.config import db
from app.main.course_form import CourseForm
from app.forms import EnrollCourseForm, DropCourseForm



main_bp = Blueprint("main", __name__, template_folder='templates')

# root route
@main_bp.route('/')
def index():
    users = {'username' : 'Jonathan'}
    return render_template("/main/index.html", users=users)

# dashboard
@main_bp.route('/dashboard')
@login_required
def dashboard():

    all_courses = Course.query.all()

    notifications = [
        "You haven’t checked Week 3 notes.",
        "New message in CMPE 102 discussion board."
    ]

    return render_template(
        "main/dashboard.html",
        courses=all_courses,
        notifications=notifications
    )


##### Routes from courses
# gets all available courses
@main_bp.route('/courses')
def courses_list():
    all_courses = Course.query.all()
    
    # checking if current user is enroller
    courses_with_status = []
    for course in all_courses:
        is_enrolled = False
        if current_user.is_authenticated:
            is_enrolled = current_user.is_enrolled_in(course)

            courses_with_status.append({
                'course': course,
                'is_enrolled': is_enrolled,
                'available_spots': course.max_students - course.get_student_count() if course.max_students else None
            })
    return render_template('main/courses_list.html', courses=courses_with_status)


## All enrolled courses
@main_bp.route('/my-courses')
@login_required
# Gets all the current user's enrolled courses
def my_courses():
    enrolled_courses = current_user.get_enrolled_courses()
    return render_template('main/my_courses.html', courses=enrolled_courses)

# Enroll in course
@main_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    # get course
    course = Course.query.get_or_404(course_id)

    # redirect if not available
    if not course.is_available():
        flash('This course is not available for enrollment.', 'danger')
        return redirect(url_for('main.courses_list'))
    
    # redirect if already enrolled
    if current_user.is_enrolled_in(course):
        flash(f'You are already enrolled in {course.title}', 'warning')
        return redirect(url_for('main.courses_list'))
    
    # enroll in course
    if current_user.enroll_in_course(course):
        db.session.commit()
        flash(f'You enrolled in {course.title}', 'success')
    else:
        flash(f'You could not enroll in {course.title}', 'danger')
    
    return redirect(url_for('main.courses_list'))
    
# Drop course
@main_bp.route('/courses/<int:course_id>/drop', methods=['POST'])
@login_required
def drop_course(course_id):
    course = Course.query.get_or_404(course_id)

    # check if user is enrolled
    if not current_user.is_enrolled_in(course):
        flash(f'You are not enrolled in {course.title}', 'warning')
        return redirect(url_for('main.my_courses'))

    # drop course
    if current_user.drop_course(course):
        db.session.commit()
        flash(f'Dropped from {course.title}', 'success')
    else: 
        flash(f'Could not drop {course.title}', 'danger')
    return redirect(url_for('main.my_courses'))


# course detail page
@main_bp.route('/courses/<int:course_id>')
# this function prints details of a specific course
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)

    is_enrolled = False
    if current_user.is_authenticated:
        is_enrolled = current_user.is_enrolled_in(course)
    
    enrolled_count = course.get_student_count()
    available_spots = None
    if course.max_students:
        available_spots = course.max_students - enrolled_count
    
    return render_template('main/course_detail.html', course=course, is_enrolled=is_enrolled, enrolled_count=enrolled_count, available_spots=available_spots)


# New courses route
@main_bp.route("/courses/new", methods=['GET','POST'])
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
@login_required
def create_course():
    course_form = CourseForm()

    if course_form.validate_on_submit():
       course_data= {
        'code' : course_form.code.data,
        'title' : course_form.title.data,
        'description': course_form.description.data, 
        'credits' : course_form.credits.data,
        'professor' : course_form.professor.data,
        'availability' : course_form.availability.data,
        'format': course_form.format.data,
        'max_students' : course_form.max_students.data
       }
       course_data.professor = current_user
       
       new_course = Course(**course_data)
       
       db.session.add(new_course)
       db.session.commit()

       flash('Course added! Check it in dashboard')
       return redirect(url_for('main.courses_list'))


    return render_template('main/new_course.html', form = course_form)


# Delete course
@main_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
@login_required
def delete_course(course_id):
    course = Course.query.filter_by(id =course_id).first()
    
    if not (current_user.is_admin or course.professor == current_user):
        abort(403)
    
    # delete course
    db.session.delete(course)
    db.session.commit()

    flash(f'Course {course.title} deleted', 'success')


# Update course
@main_bp.route('/courses/<int:course_id>/update', methods=['GET', 'POST'])
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
@login_required
def update_course(course_id):

    course_info = Course.query.filter_by(id=course_id).first()
    course_form = CourseForm()

    if not (current_user.is_admin or course.professor == current_user):
        abort(403)

    # Pre-populate form on GET request
    if request.method == 'GET' and course_info: 
        course_form.code.data = course_info.code
        course_form.title.data = course_info.title
        course_form.description.data = course_info.description
        course_form.credits.data = course_info.credits
        course_form.professor.data = course_info.professor
        course_form.availability.data = course_info.availability
        course_form.format.data = course_info.format
        course_form.max_students.data = course_info.max_students
    # Updating all fields
    if course_form.validate_on_submit():
       course_info.code = course_form.code.data
       course_info.title = course_form.title.data
       course_info.description = course_form.description.data
       course_info.credits = course_form.credits.data
       course_info.professor = course_form.professor.data
       course_info.availability = course_form.availability.data
       course_info.format = course_form.format.data
       course_info.max_students = course_form.max_students.data
       db.session.add(course_info)
       db.session.commit()

       flash('Course updated! Check it in dashboard', 'success')
       return redirect(url_for('main.courses_list'))

    return render_template('main/update_course.html', form=course_form, course_info=course_info)
# GPA calculator 
@main_bp.route('/gpa')
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

# Assignments
@main_bp.route('/courses/<int:course_id>/assignments')
@login_required
def assignments_list(course_id):
    # real assignment details
    
    fake_assignments = [
        {
            "id": 1,
            "title": "Homework 1",
            "due_date": "2025-03-10",
            "points": 100,
            "status": "Submitted"
        },
        {
            "id": 2,
            "title": "Project Proposal",
            "due_date": "2025-03-15",
            "points": 50,
            "status": "Not submitted"
        },
    ]

    return render_template(
        "main/assignments_list.html",
        course_id=course_id,
        assignments=fake_assignments
    )