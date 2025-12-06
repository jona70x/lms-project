from flask import render_template, Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Course, User, Assignment
from app.config import db
from app.main.course_form import CourseForm
from app.forms import EnrollCourseForm, DropCourseForm
from app.assignments.assignment_form import AssignmentForm


assignments_bp = Blueprint("assignments", __name__, template_folder='templates')

#displays all the assignments by course
@assignments_bp.route('/')
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
@login_required
def create_assignment():
    form = AssignmentForm()

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

        return redirect(url_for('assignments.index'))
    
    return render_template('assignments/new_assignment.html', form=form)


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