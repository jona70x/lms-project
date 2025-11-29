from flask import render_template, Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Course, User
from app.config import db
from app.forms import EnrollCourseForm, DropCourseForm



main_bp = Blueprint("main", __name__, template_folder='templates')

# root route
@main_bp.route('/')
def index():
    users = {'username' : 'Jonathan'}
    return render_template("/main/index.html", users=users)

# dashboard
@main_bp.route('/dashboard')
def dashboard():
    return render_template("/main/dashboard.html")


##### Routes from courses
# gets all available courses
@main_bp.route('courses')
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

