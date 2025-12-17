from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models import Course


class AnnouncementForm(FlaskForm):
    course_id = SelectField('Select course', coerce=int, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Announcement', render_kw={"class": "btn btn-primary border-primary-subtle"})
    update = SubmitField('Update Announcement', render_kw={"class": "btn btn-secondary border-secondary-subtle"})
    cancel = SubmitField('Cancel', render_kw={"class": "btn btn-danger border-danger-subtle"})

    def __init__(self, *args, **kwargs):
        super(AnnouncementForm, self).__init__(*args, **kwargs)
        self.course_id.choices = [(course.id, f"{course.code} - {course.title}") for course in Course.query.all()]
