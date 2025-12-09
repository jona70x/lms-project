from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import Course

class CourseForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=6)])
    description = TextAreaField('Description')
    credits = IntegerField('Credits', [DataRequired()])
    professor = StringField('Professor', [DataRequired()])
    availability = BooleanField('Availability', default=False)
    format = SelectField('Format', choices=['online', 'in-person'])
    max_students = IntegerField('Maximux Students', [DataRequired()])
    submit = SubmitField('Create course', render_kw={"class": "btn btn-primary border-primary-subtle"})
    update = SubmitField('Update course', render_kw={"class": "btn btn-primary border-primary-subtle"})
    cancel = SubmitField('Cancel', render_kw={"class": "btn btn-danger border-danger-subtle"})

    def set_data(self):
        pass



"""
  {
            'code': 'PHYS51',
            'title': 'General Physics II',
            'description': 'A calculus-based introduction to electricity and magnetism, covering electric charges, electric and magnetic fields, dc and ac circuits, and electromagnetic waves.',
            'credits': 4,
            'professor': 'John Doe',
            'availability': True,
            'format': 'online',
            'max_students': 30
        },
""" 