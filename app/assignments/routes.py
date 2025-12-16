from flask import render_template, Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Course, User, Assignment
from app.config import db
from app.assignments.assignment_form import AssignmentForm


assignments_bp = Blueprint("assignments", __name__, template_folder='templates')

#displays all the assignments by course
@assignments_bp.route('/')
@login_required
def index():
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
    
    # Pre-select course if course_id is provided
    if course_id and request.method == 'GET':
        form.course_id.data = course_id

    if form.validate_on_submit():
        # extracting form data
        assignment_data = {
            'course_id': form.course_id.data,
            'title' : form.title.data,
            'description': form.description.data,
            'due_date': form.due_date.data,
            'max_points': form.max_points.data
        }

        new_assignment = Assignment(**assignment_data)

        db.session.add(new_assignment)
        db.session.commit()

        flash('Assignment created!', 'success')
        
        # Redirect back to course dashboard if course_id was provided
        if course_id:
            return redirect(url_for('courses.course_dashboard', course_id=course_id, tab='assignments'))

        return redirect(url_for('assignments.index'))
    
    return render_template('assignments/new_assignment.html', form=form, course_id=course_id)


# Assignment detail page
@assignments_bp.route('/<int:assignment_id>')
@login_required
def assignment_detail(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course  # Get the course using the relationship backref
    
    return render_template('assignments/assignment_details.html', assignment=assignment, course=course)


# deletes assignment
@assignments_bp.route('/<int:assignment_id>/delete', methods=['POST'])
@login_required
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    flash('success, assignment deleted', 'success')

    return redirect(url_for('assignments.index'))

@assignments_bp.route('/<int:assignment_id>/edit', methods=['GET','POST'])
@assignments_bp.route('/<int:assignment_id>/update', methods=['GET','POST'])
@login_required
def update_assignment(assignment_id):

    assignment = Assignment.query.filter_by(id=assignment_id).first()
    course = assignment.course
    form = AssignmentForm()

    # Pre-populate form on GET request
    if request.method == 'GET' and assignment: 
        form.course_id.data = course.id
        form.title.data = assignment.title
        form.description.data = assignment.description
        form.max_points.data = assignment.max_points
        form.due_date.data = assignment.due_date
    
    # Updating all fields
    if form.validate_on_submit():
       assignment.course_id = form.course_id.data
       assignment.title = form.title.data
       assignment.description = form.description.data
       assignment.max_points = form.max_points.data
       assignment.due_date = form.due_date.data
       db.session.add(assignment)
       db.session.commit()

       flash('Assignment edited! Check it on the assignments list', 'success')
       return redirect(url_for('assignments.assignment_detail', assignment_id=assignment.id))

    return render_template('assignments/update_assignment.html', form=form, assignment=assignment)

