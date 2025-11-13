from app.config import db
from datetime import datetime


# User Model

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    avatar_url = db.Column(db.String(400), nullable=False)
    role = db.Column(db.String(32), default='student') # role could be student | instructor | admin
    created_at = db.Column(db.DateTime, default = datetime.timezone.utc, nullable=False)

# Course Model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text)
    instructor = db.Column(db.String(32), nullable=False)
    enrollments = db.Column(db.Integer, nullable=False)
    num_units = db.Column(db.Integer, nullable=False)




