from app import create_app
from app.config import db
from app.models import User

# create_app is already a Flask instance, not a function
with create_app.app_context():
    # Drop all tables and recreate 
    db.drop_all()
    db.create_all()
    print("Database tables created successfully")
    
    # Create test user
    test_user = User(
        email='test@example.com',
        avatar_url='https://ui-avatars.com/api/?name=Test+User',
        role='student'
    )
    test_user.set_password('password123')  # Test password
    
    db.session.add(test_user)
    db.session.commit()
    
    print("Test user created")