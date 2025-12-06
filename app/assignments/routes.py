from flask import render_template, Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Course, User, Assignment
from app.config import db
from app.main.course_form import CourseForm
from app.forms import EnrollCourseForm, DropCourseForm
from app.assignments.assignment_form import AssignmentForm


assignments_bp = Blueprint("assignments", __name__, template_folder='templates')

@assignments_bp.route('/')
def index():
    return '<h1>Working</h1>'


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

        return redirect(url_for('main.index'))
    
    return render_template('assignments/new_assignment.html', form=form)