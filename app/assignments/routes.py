from flask import render_template, Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Course, User, Assignment, StudentAssignment
from app.config import db
from app.assignments.assignment_form import AssignmentForm
from app.assignments.grade_form import GradeForm
from app.decorators import roles_required


assignments_bp = Blueprint("assignments", __name__, template_folder='templates')

#displays all the assignments by course -- Only admins can access this page
@assignments_bp.route('/')
@login_required
def index():
    if not current_user.is_admin:
        flash("You don't have access", 'danger')
        return redirect(url_for('main.index'))
    
    all_courses = Course.query.all()

    courses_with_assignments = []
    for course in all_courses:
        assignments = course.assignments.all()

        courses_with_assignments.append({
            'course': course,
            'assignments': assignments,
            'assignment_count': len(assignments)
        })
    
    return render_template('assignments/assignments_list.html', courses_with_assignments=courses_with_assignments)


#create new assignment route
@assignments_bp.route('/new', methods=['GET', 'POST'])
@assignments_bp.route('/new/<int:course_id>', methods=['GET', 'POST'])
@login_required
def create_assignment(course_id=None):
    form = AssignmentForm()
    course = None
    
    # get the course of there is an id
    if course_id:
        course = Course.query.get_or_404(course_id)
        form.course_id.data = course_id

    if form.validate_on_submit():
        final_course_id = course_id if course_id else form.course_id.data
    
        assignment_data = {
            'course_id': final_course_id,
            'title' : form.title.data,
            'description': form.description.data,
            'due_date': form.due_date.data,
            'max_points': form.max_points.data
        }

        new_assignment = Assignment(**assignment_data)

        db.session.add(new_assignment)
        db.session.commit()

        flash('Assignment created!', 'success')
        
        if course_id:
            return redirect(url_for('courses.course_dashboard', course_id=course_id, tab='assignments'))

        return redirect(url_for('assignments.index'))
    
    return render_template('assignments/new_assignment.html', form=form, course_id=course_id, course=course)


# Assignment detail page
@assignments_bp.route('/<int:assignment_id>')
@login_required
def assignment_detail(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course 
    
    return render_template('assignments/assignment_details.html', assignment=assignment, course=course)


# deletes assignment
@assignments_bp.route('/<int:assignment_id>/delete', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    # Only course owner or admin can delete assignments
    if not (course.professor_id == current_user.id or current_user.is_admin):
        flash("You don't have permission to delete this assignment.", 'danger')
        return redirect(url_for('assignments.assignment_detail', assignment_id=assignment_id))
    
    db.session.delete(assignment)
    db.session.commit()
    flash('Assignment deleted successfully!', 'success')

    return redirect(url_for('courses.course_dashboard', course_id=course.id, tab='assignments'))

@assignments_bp.route('/<int:assignment_id>/edit', methods=['GET','POST'])
@assignments_bp.route('/<int:assignment_id>/update', methods=['GET','POST'])
@login_required
def update_assignment(assignment_id):

    assignment = Assignment.query.filter_by(id=assignment_id).first()
    course = assignment.course
    
    # Only course owner or admin can update assignments
    if not (course.professor_id == current_user.id or current_user.is_admin):
        flash("You don't have permission to update this assignment.", 'danger')
        return redirect(url_for('assignments.assignment_detail', assignment_id=assignment_id))
    
    form = AssignmentForm()

    if request.method == 'GET' and assignment: 
        form.course_id.data = course.id
        form.title.data = assignment.title
        form.description.data = assignment.description
        form.max_points.data = assignment.max_points
        form.due_date.data = assignment.due_date
    

    if form.validate_on_submit():
       assignment.title = form.title.data
       assignment.description = form.description.data
       assignment.max_points = form.max_points.data
       assignment.due_date = form.due_date.data
       db.session.commit()

       flash('Assignment edited! Check it on the assignments list', 'success')
       return redirect(url_for('assignments.assignment_detail', assignment_id=assignment.id))

    return render_template('assignments/update_assignment.html', form=form, assignment=assignment, course=course)


# View all submissions for an assignment (instructors only)
@assignments_bp.route('/<int:assignment_id>/submissions')
@login_required
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
def assignment_submissions(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    # Checking if user is the course owner or admin
    if not (course.professor_id == current_user.id or current_user.is_admin):
        flash("You don't have access to view these submissions.", 'danger')
        return redirect(url_for('courses.course_dashboard', course_id=course.id))
    
   # all completed assginments 
    submissions = StudentAssignment.query.filter_by(
        assignment_id=assignment_id
    ).all()
    
    return render_template(
        'assignments/assignment_submissions.html',
        assignment=assignment,
        course=course,
        submissions=submissions
    )


# Grade the submissions
@assignments_bp.route('/<int:assignment_id>/grade/<int:student_id>', methods=['GET', 'POST'])
@login_required
@roles_required(User.ROLE_PROFESSOR, User.ROLE_ADMIN)
def grade_submission(assignment_id, student_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    student = User.query.get_or_404(student_id)
    
    # Check if user is the course owner or admin
    if not (course.professor_id == current_user.id or current_user.is_admin):
        flash("You don't have access to grade this submission.", 'danger')
        return redirect(url_for('courses.course_dashboard', course_id=course.id))
    
    student_assignment = StudentAssignment.query.filter_by(
        assignment_id=assignment_id,
        user_id=student_id
    ).first()
    
    if not student_assignment:
        flash("This student hasn't submitted this assignment yet.", 'warning')
        return redirect(url_for('assignments.assignment_submissions', assignment_id=assignment_id))
    
    form = GradeForm()
    
    if request.method == 'GET' and student_assignment.score is not None:
        form.score.data = student_assignment.score
    
    if form.validate_on_submit():
        score = form.score.data
        
        if score < 0 or score > assignment.max_points:
            flash(f'Score must be between 0 and {assignment.max_points}.', 'danger')
            return render_template(
                'assignments/grade_submission.html',
                form=form,
                assignment=assignment,
                course=course,
                student=student,
                student_assignment=student_assignment
            )
        
        student_assignment.score = score
        db.session.commit()
        
        flash(f'Grade submitted for {student.email}!', 'success')
        return redirect(url_for('assignments.assignment_submissions', assignment_id=assignment_id))
    
    return render_template(
        'assignments/grade_submission.html',
        form=form,
        assignment=assignment,
        course=course,
        student=student,
        student_assignment=student_assignment
    )
