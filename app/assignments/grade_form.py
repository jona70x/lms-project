from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class GradeForm(FlaskForm):
    score = IntegerField('Score', validators=[InputRequired(message="Score is required"), NumberRange(min=0, message="Score must be at least 0")])
    submit = SubmitField('Submit Grade', render_kw={"class": "btn btn-primary border-primary-subtle"})
