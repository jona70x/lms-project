from app import create_app
from app.config import db
from app.models import User, Course, Assignment, Enrollment, StudentAssignment

# create_app is already a Flask instance, not a function
with create_app.app_context():
    # Drop all tables and recreate 
    db.drop_all()
    db.create_all()
    print("Database tables created successfully")
    
    # Create test user (admin)
    user_test_admin = User(
        email='test@admin.com',
        avatar_url='https://ui-avatars.com/api/?name=Test+User',
        role='admin'
    )
    user_test_admin.set_password('password123')  # Test password

    # Create test user (student)
    user_test_student = User(
        email='test@student.com',
        avatar_url='https://ui-avatars.com/api/?name=Test+User',
        role='student'
    )
    user_test_student.set_password('password123')  # Test password

    # Create test user (professor)
    user_test_professor = User(
        email='test@professor.com',
        avatar_url='https://ui-avatars.com/api/?name=Test+User',
        role='professor'
    )
    user_test_professor.set_password('password123')  # Test password
    
    db.session.add(user_test_admin)
    db.session.add(user_test_student)
    db.session.add(user_test_professor)
    db.session.commit()
    
    print("Test users created")