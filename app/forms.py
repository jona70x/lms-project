from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    # username = StringField("Username", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary border-primary-subtle", })

"""Registration Form Class"""
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    # Role selection
    role = SelectField(
        'Register as a',
        choices=[
            (User.ROLE_STUDENT, 'Student'),
            (User.ROLE_PROFESSOR, 'Professor'),
            (User.ROLE_ADMIN, 'Admin'),
        ],
        default=User.ROLE_STUDENT,
        validators=[DataRequired()],
    )
    
    submit = SubmitField('Register')
    
    # custom validators
    def validate_email(self, email):
        # check if email already exists
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already registered. Please use another')
        
"""Enroll in course form in detil page to enroll. Just a submit button
""" 
class EnrollCourseForm(FlaskForm):
    submit = SubmitField('Enroll in course')
"""Form to drop if user is enrolled in course"""
class DropCourseForm(FlaskForm):
    submit = SubmitField("Drop Course")