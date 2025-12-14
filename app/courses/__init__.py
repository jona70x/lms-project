from flask import abort, render_template, Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.decorators import roles_required
from app.models import Course, User, Assignment
from app.config import db
from app.courses.course_form import CourseForm
from app.forms import EnrollCourseForm, DropCourseForm



courses_bp = Blueprint("courses", __name__, template_folder='templates')

# Import routes to register them with the blueprint
from app.courses import routes
