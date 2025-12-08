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
    avatar_url = db.Column(db.String(400), nullable=True)
    role = db.Column(db.String(32), default='student')  # role could be student | instructor | admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # course relationship
    courses = db.relationship('Course', secondary='enrollments', backref='students', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # to check if student or professor
    # def is_professor(self):
    #     return self.role == 'professor'
    
    # def is_student(self):
    #     return self.role == 'student'
    
    ### methods for course management

    ## enrolls this student in a course
    def enroll_in_course(self, course):
        if not self.is_enrolled_in(course):
            enrollment = Enrollment(user_id=self.id, course_id=course.id)
            db.session.add(enrollment)
            return True
        return False # already enrolled  
    
    # drops the course for user. returns true if we drop course, false if we were not enrolled.
    def drop_course(self,course):
        enrollment = Enrollment.query.filter_by(user_id=self.id, course_id=course.id).first()
        if enrollment:
            db.session.delete(enrollment)
            return True
        return False 
    
    # check if user is enrolled in course
    def is_enrolled_in(self, course):
        return Enrollment.query.filter_by(user_id=self.id, course_id=course.id).first() is not None
    
    ## returns all the courses where students are enrolled in
    def get_enrolled_courses(self):
        return Course.query.join(Enrollment).filter(Enrollment.user_id == self.id).all()
    
    # returns all number of enrolled courses
    def get_enrolled_courses_count(self):
        return len(self.course_enrollments)
    
    # For course management (professor role)
    # def get_created_courses(self):
    #     return Course.query.filter_by(professor_id=id).all()

    def __repr__(self):
        return f"<User {self.email}>"

# Course Model
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)  # number of units/credits
    professor = db.Column(db.String(128), nullable=False)
    # professor_id = db.Column(db.Integer, db.ForeignKey('users.id')) # id of user who created the course
    availability = db.Column(db.Boolean, default=True)
    format = db.Column(db.String(32), default='online')
    max_students = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # many-to-many relationships with User through Enrollment 
    enrollments_rel = db.relationship('Enrollment', backref='course', lazy='dynamic', cascade='all,delete-orphan')

    # Methods 
    # gets all students enrolled in this course
    def get_enrolled_students(self):
        return User.query.join(Enrollment).filter(Enrollment.course_id == self.id).all()
    
    # gets all enrolled students
    def get_student_count(self):
        return self.enrollments_rel.count()
    
    # checks if we can enroll in a course
    def is_available(self):
        return self.availability and (self.max_students is None or self.get_student_count() < self.max_students)
    #Course relationship
    assignments = db.relationship('Assignment', backref='course', lazy='dynamic', cascade='all,delete-orphan')

    # course management
    # relationship with professor
    # professor = db.relationship('User', foreign_keys=[professor_id], backref='created_courses')
    
    def __repr__(self):
        return f'<Course {self.code}: {self.title}'

# class to track student enrollment in courses
class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    # columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(2))

    #Relationships
    user = db.relationship('User', backref='course_enrollments')

    # to avoid duplicates
    __table_args__ = (db.UniqueConstraint('user_id', "course_id", name='unique_user_course'),)

    def __repr__(self):
        return f'<Enrollment: User {self.user_id} -> Course {self.course_id}>'


# Assignmnets model
class Assignment(db.Model):
    __tablename__ = "assignments"

    id= db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    #assignment info
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False )
    due_date= db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    max_points = db.Column(db.Integer, default=100)

    def __repr__(self):
        return f'<Assignment {self.title} for Course {self.course_id}>'


