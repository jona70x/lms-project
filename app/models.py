from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import db
from datetime import datetime


# User Model
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    ROLE_STUDENT = "student"
    ROLE_PROFESSOR = "professor"
    ROLE_ADMIN = "admin"

    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    avatar_url = db.Column(db.String(400), nullable=True)
    role = db.Column(db.String(32), default=ROLE_STUDENT, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # many-to-many student side
    courses = db.relationship(
        "Course",
        secondary="enrollments",
        backref="students",
        lazy="dynamic",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ---- role helpers ----
    @property
    def is_student(self):
        return self.role == self.ROLE_STUDENT

    @property
    def is_professor(self):
        return self.role == self.ROLE_PROFESSOR

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    # ---- course enrollment helpers (student) ----
    def enroll_in_course(self, course):
        from app.models import Enrollment  # avoid circular import at top-level
        if not self.is_enrolled_in(course):
            enrollment = Enrollment(user_id=self.id, course_id=course.id)
            db.session.add(enrollment)
            return True
        return False

    def drop_course(self, course):
        from app.models import Enrollment
        enrollment = Enrollment.query.filter_by(
            user_id=self.id,
            course_id=course.id
        ).first()
        if enrollment:
            db.session.delete(enrollment)
            return True
        return False

    def is_enrolled_in(self, course):
        from app.models import Enrollment
        return Enrollment.query.filter_by(
            user_id=self.id,
            course_id=course.id
        ).first() is not None

    def get_enrolled_courses(self):
        from app.models import Course, Enrollment
        return Course.query.join(Enrollment).filter(
            Enrollment.user_id == self.id
        ).all()

    def get_enrolled_courses_count(self):
        from app.models import Enrollment
        return Enrollment.query.filter_by(user_id=self.id).count()

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

    # keep existing DB column name
    professor = db.Column(db.String(128), nullable=True)

    # link to professor user (relationship has a DIFFERENT name)
    professor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    professor_user = db.relationship(
        'User',
        foreign_keys=[professor_id],
        backref='created_courses'
    )

    availability = db.Column(db.Boolean, default=True)
    format = db.Column(db.String(32), default='online')
    max_students = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    enrollments_rel = db.relationship(
        'Enrollment',
        backref='course',
        lazy='dynamic',
        cascade='all,delete-orphan'
    )

    assignments = db.relationship(
        'Assignment',
        back_populates='course',
        lazy='dynamic',
        cascade='all,delete-orphan'
    )

    def get_enrolled_students(self):
        return User.query.join(Enrollment).filter(
            Enrollment.course_id == self.id
        ).all()

    def get_student_count(self):
        return self.enrollments_rel.count()

    def is_available(self):
        return self.availability and (
            self.max_students is None
            or self.get_student_count() < self.max_students
        )

    def __repr__(self):
        return f'<Course {self.code}: {self.title}>'

# class to track student enrollment in courses
class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(2))

    # Relationships
    user = db.relationship('User', backref='course_enrollments')

    # to avoid duplicates
    __table_args__ = (
        db.UniqueConstraint('user_id', "course_id", name='unique_user_course'),
    )

    def __repr__(self):
        return f'<Enrollment: User {self.user_id} -> Course {self.course_id}>'


# Assignments model
class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    # assignment info
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    max_points = db.Column(db.Integer, default=100)

    # relationship back to Course
    course = db.relationship('Course', back_populates='assignments')
    
    # relationship to student progress
    student_assignments = db.relationship(
        'StudentAssignment',
        back_populates='assignment',
        lazy='dynamic',
        cascade='all,delete-orphan'
    )

  # Get the status of this assignment for a specific student
    def get_student_status(self, user_id):
        student_assignment = StudentAssignment.query.filter_by(
            assignment_id=self.id,
            user_id=user_id
        ).first()
        if student_assignment:
            return student_assignment.status
        return 'Not Started'

    def __repr__(self):
        return f'<Assignment {self.title} for Course {self.course_id}>'


# Model to track individual student progress on assignments
class StudentAssignment(db.Model):
    __tablename__ = "student_assignments"

    STATUS_NOT_STARTED = "Not Started"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_COMPLETED = "Completed"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    
    status = db.Column(db.String(32), default=STATUS_NOT_STARTED, nullable=False)
    score = db.Column(db.Integer, nullable=True)  # Grade received (if graded)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships
    user = db.relationship('User', backref='student_assignments')
    assignment = db.relationship('Assignment', back_populates='student_assignments')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'assignment_id', name='unique_user_assignment'),
    )

    # status functions
    def mark_completed(self, score=None):
        self.status = self.STATUS_COMPLETED
        self.completed_at = datetime.utcnow()
        if score is not None:
            self.score = score
        elif self.assignment:
            self.score = self.assignment.max_points

    def mark_in_progress(self):
        self.status = self.STATUS_IN_PROGRESS
        self.completed_at = None
       

    def mark_not_started(self):
        self.status = self.STATUS_NOT_STARTED
        self.completed_at = None
        self.score = None  

    def __repr__(self):
        return f'<StudentAssignment: User {self.user_id} -> Assignment {self.assignment_id} ({self.status})>'

class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
