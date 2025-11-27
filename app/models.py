from flask_login import UserMixin  # track auth/session helpers
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import db
from datetime import datetime

# User Model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    avatar_url = db.Column(db.String(400), nullable=False)
    role = db.Column(db.String(32), default='student')  # role could be student | instructor | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.email}>"

# Course Model
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text)
    instructor = db.Column(db.String(32), nullable=False)
    enrollments = db.Column(db.Integer, nullable=False)
    num_units = db.Column(db.Integer, nullable=False)



