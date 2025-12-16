from flask import abort, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.decorators import roles_required
from app.models import Course, User, Assignment, Enrollment, StudentAssignment, Announcement
from app.config import db
from app.courses.course_form import CourseForm
from app.courses import courses_bp


# gets all available courses
@courses_bp.route('/')
def courses_list():
    all_courses = Course.query.all()
    
    # checking if current user is enrolled
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
    return render_template('courses/courses_list.html', courses=courses_with_status)


# Gets all the current user's enrolled courses
@courses_bp.route('/my-courses')
@login_required
def my_courses():
    enrolled_courses = current_user.get_enrolled_courses()
    return render_template('courses/my_courses.html', courses=enrolled_courses)


# Courses created by the current user (for professors/admins)
@courses_bp.route('/my-created-courses')
@login_required
@roles_required('professor', 'admin')
def my_created_courses():
    """Gets all courses created by the current user (professor/admin)"""
    created_courses = Course.query.filter_by(professor_id=current_user.id).all()
    return render_template('courses/my_created_courses.html', courses=created_courses)


# Enroll in course
@courses_bp.route('/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    # get course
    course = Course.query.get_or_404(course_id)

    # redirect if not available
    if not course.is_available():
        flash('This course is not available for enrollment.', 'danger')
        return redirect(url_for('courses.courses_list'))
    
    # redirect if already enrolled
    if current_user.is_enrolled_in(course):
        flash(f'You are already enrolled in {course.title}', 'warning')
        return redirect(url_for('courses.courses_list'))
    
    # enroll in course
    if current_user.enroll_in_course(course):
        db.session.commit()
        flash(f'You enrolled in {course.title}', 'success')
    else:
        flash(f'You could not enroll in {course.title}', 'danger')
    
    return redirect(url_for('courses.courses_list'))

    
# Drop course
@courses_bp.route('/<int:course_id>/drop', methods=['POST'])
@login_required
def drop_course(course_id):
    course = Course.query.get_or_404(course_id)

    # check if user is enrolled
    if not current_user.is_enrolled_in(course):
        flash(f'You are not enrolled in {course.title}', 'warning')
        return redirect(url_for('courses.my_courses'))

    # drop course
    if current_user.drop_course(course):
        db.session.commit()
        flash(f'Dropped from {course.title}', 'success')
    else: 
        flash(f'Could not drop {course.title}', 'danger')
    return redirect(url_for('courses.my_courses'))


# course detail page
@courses_bp.route('/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)

    is_enrolled = False
    if current_user.is_authenticated:
        is_enrolled = current_user.is_enrolled_in(course)
    
    enrolled_count = course.get_student_count()
    available_spots = None
    if course.max_students:
        available_spots = course.max_students - enrolled_count
    
    return render_template('courses/course_detail.html', course=course, is_enrolled=is_enrolled, enrolled_count=enrolled_count, available_spots=available_spots)


# toggles assignment status for student
@courses_bp.route('/<int:course_id>/assignment/<int:assignment_id>/toggle-status', methods=['POST'])
@login_required
def toggle_assignment_status(course_id, assignment_id):
    course = Course.query.get_or_404(course_id)
    assignment = Assignment.query.get_or_404(assignment_id)
    
    if assignment.course_id != course_id:
        flash('Invalid assignment for this course.', 'danger')
        return redirect(url_for('courses.course_dashboard', course_id=course_id, tab='assignments'))
    # checking if user is enrolled 
    if not current_user.is_enrolled_in(course):
        flash('You must be enrolled in this course to update assignment status.', 'warning')
        return redirect(url_for('courses.course_dashboard', course_id=course_id, tab='assignments'))

    student_assignment = StudentAssignment.query.filter_by(
        user_id=current_user.id,
        assignment_id=assignment_id
    ).first()
    
    if not student_assignment:
        student_assignment = StudentAssignment(
            user_id=current_user.id,
            assignment_id=assignment_id,
            status=StudentAssignment.STATUS_NOT_STARTED
        )
        db.session.add(student_assignment)
    
    # toggling status: Not Started -> In Progress -> Completed -> Not Started
    if student_assignment.status == StudentAssignment.STATUS_NOT_STARTED:
        student_assignment.mark_in_progress()
        flash(f'"{assignment.title}" marked as In Progress.', 'info')
    elif student_assignment.status == StudentAssignment.STATUS_IN_PROGRESS:
        student_assignment.mark_completed() 
        flash(f'"{assignment.title}" marked as Completed! You earned {assignment.max_points}/{assignment.max_points} points.', 'success')
    else:
        student_assignment.mark_not_started()
        flash(f'"{assignment.title}" reset to Not Started. Score cleared.', 'secondary')
    
    db.session.commit()
    
    return redirect(url_for('courses.course_dashboard', course_id=course_id, tab='assignments'))


# course dashboard 
@courses_bp.route('/<int:course_id>/dashboard')
@courses_bp.route('/<int:course_id>/dashboard/<tab>')
@login_required
def course_dashboard(course_id, tab='assignments'):
    course = Course.query.get_or_404(course_id)
    
    is_enrolled = current_user.is_enrolled_in(course)
    is_course_owner = course.professor_id == current_user.id
    
    # only enrolled students, professor owner, or admins can view
    if not (is_enrolled or is_course_owner or current_user.is_admin):
        flash('You must be enrolled in this course to view the dashboard.', 'warning')
        return redirect(url_for('courses.course_detail', course_id=course_id))
    
    enrolled_count = course.get_student_count()
    enrolled_students = course.get_enrolled_students()
    assignments_query = Assignment.query.filter_by(course_id=course_id).order_by(Assignment.due_date).all()
    
    assignments = []
    for assignment in assignments_query:
        student_assignment = StudentAssignment.query.filter_by(
            assignment_id=assignment.id,
            user_id=current_user.id
        ).first()
        
        status = student_assignment.status if student_assignment else 'Not Started'
        score = student_assignment.score if student_assignment else None
        
        assignment_data = {
            'id': assignment.id,
            'title': assignment.title,
            'description': assignment.description,
            'due_date': assignment.due_date,
            'max_points': assignment.max_points,
            'status': status,
            'score': score
        }
        assignments.append(type('Assignment', (), assignment_data)())
    
    # grades based on student's completed assignments
    total_points_possible = sum(a.max_points for a in assignments_query) if assignments_query else 0
    total_points_earned = sum(
        sa.score for sa in StudentAssignment.query.filter_by(user_id=current_user.id).all()
        if sa.score is not None and sa.assignment.course_id == course_id
    )
    current_grade = (total_points_earned / total_points_possible * 100) if total_points_possible > 0 else 0
    
    # Calculate letter grade
    if current_grade >= 90:
        letter_grade = 'A'
    elif current_grade >= 80:
        letter_grade = 'B'
    elif current_grade >= 70:
        letter_grade = 'C'
    elif current_grade >= 60:
        letter_grade = 'D'
    else:
        letter_grade = 'F'
    
    # Get announcements for this course from the database
    announcements = Announcement.query.filter_by(course_id=course_id).order_by(Announcement.created_at.desc()).all()
    
    # Get all student submissions for this course 
    student_submissions = {}
    if is_course_owner or current_user.is_admin:
        all_submissions = StudentAssignment.query.join(Assignment).filter(
            Assignment.course_id == course_id
        ).all()
        for submission in all_submissions:
            student_submissions[(submission.assignment_id, submission.user_id)] = submission
    
    return render_template(
        'courses/course_dashboard.html',
        course=course,
        is_enrolled=is_enrolled,
        is_course_owner=is_course_owner,
        enrolled_count=enrolled_count,
        enrolled_students=enrolled_students,
        assignments=assignments,
        active_tab=tab,
        total_points_earned=total_points_earned,
        total_points_possible=total_points_possible,
        current_grade=round(current_grade, 1),
        letter_grade=letter_grade,
        announcements=announcements,
        student_submissions=student_submissions
    )


# New courses route
@courses_bp.route("/new", methods=['GET','POST'])
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
@login_required
def create_course():
    course_form = CourseForm()

    if course_form.validate_on_submit():
       # Check if course code already exists
       existing_course = Course.query.filter_by(code=course_form.code.data).first()
       if existing_course:
           flash('A course with this ID already exists. Please change the ID.', 'danger')
           return render_template('courses/new_course.html', form=course_form)
       
       course_data= {
        'code' : course_form.code.data,
        'title' : course_form.title.data,
        'description': course_form.description.data, 
        'credits' : course_form.credits.data,
        'professor' : course_form.professor.data,
        'professor_id' : current_user.id,
        'availability' : course_form.availability.data,
        'format': course_form.format.data,
        'max_students' : course_form.max_students.data
       }
       
       new_course = Course(**course_data)
       
       db.session.add(new_course)
       db.session.commit()

       flash('Course added! Check it in dashboard')
       return redirect(url_for('courses.courses_list'))


    return render_template('courses/new_course.html', form=course_form)


# Delete course
@courses_bp.route('/<int:course_id>/delete', methods=['POST'])
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
@login_required
def delete_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    
    if not (current_user.is_admin or course.professor_user == current_user):
        abort(403)
    
    # delete course
    db.session.delete(course)
    db.session.commit()

    flash(f'Course {course.title} deleted', 'success')
    return redirect(url_for('courses.courses_list'))


# Update course
@courses_bp.route('/<int:course_id>/update', methods=['GET', 'POST'])
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
@login_required
def update_course(course_id):

    course_info = Course.query.filter_by(id=course_id).first()
    course_form = CourseForm()

    if not (current_user.is_admin or course_info.professor_user == current_user):
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
       # Check if course code already exists (and it's not the current course)
       existing_course = Course.query.filter_by(code=course_form.code.data).first()
       if existing_course and existing_course.id != course_info.id:
           flash('A course with this ID already exists. Please change the ID.', 'danger')
           return render_template('courses/update_course.html', form=course_form, course_info=course_info)
       
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
       return redirect(url_for('courses.courses_list'))

    return render_template('courses/update_course.html', form=course_form, course_info=course_info)
