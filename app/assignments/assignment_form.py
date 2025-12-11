from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import Course

class AssignmentForm(FlaskForm):
    course_id = SelectField('Select course', coerce=int, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    due_date = DateField('Due date', format='%Y-%m-%d', validators=[Optional()])
    max_points = IntegerField('Max grade points', validators=[DataRequired()], default=100)
    submit = SubmitField('Create Assignment', render_kw={"class": "btn btn-primary border-primary-subtle"})
    update = SubmitField('Update Assignment', render_kw={"class": "btn btn-secondary border-secondary-subtle"})
    cancel = SubmitField('Cancel', render_kw={"class": "btn btn-danger border-danger-subtle"})

    # adds courses to dropdown
    def __init__(self,*args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)

        self.course_id.choices = [(course.id, f"{course.code} - {course.title}") for course in Course.query.all()]



   
"""
 id= db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    #assignment info
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False )
    due_date= db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    max_points = db.Column(db.Integer, default=100)
    """