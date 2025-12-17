from app import create_app
from app.config import db
from app.models import User

DEFAULT_PASSWORD = "password123"  # demo password

def populate_users():
    app = create_app()

    with app.app_context():
        # Start from a clean database
        db.drop_all()
        db.create_all()
        print("Database tables created successfully")

        users_data = [
            # Demo admins
            {"email": "test@admin.com",                "role": User.ROLE_ADMIN},
            {"email": "admin@intelligrades.test",      "role": User.ROLE_ADMIN},

            # Demo professors
            {"email": "test@professor.com",           "role": User.ROLE_PROFESSOR},
            {"email": "john.doe@university.edu",      "role": User.ROLE_PROFESSOR},
            {"email": "carlos.rojas@university.edu",  "role": User.ROLE_PROFESSOR},
            {"email": "michael.green@university.edu", "role": User.ROLE_PROFESSOR},
            {"email": "emily.samson@university.edu",  "role": User.ROLE_PROFESSOR},
            {"email": "david.bee@university.edu",     "role": User.ROLE_PROFESSOR},
            {"email": "taylor.dave@university.edu",   "role": User.ROLE_PROFESSOR},
            

            # Demo student (there are also other demo students in populate_courses)
            {"email": "test@student.com",             "role": User.ROLE_STUDENT},
        ]

        for data in users_data:
            user = User(
                email=data["email"],
                avatar_url=f"https://ui-avatars.com/api/?name={data['email']}",
                role=data["role"],
            )
            user.set_password(DEFAULT_PASSWORD)
            db.session.add(user)

        db.session.commit()
        print(f"{len(users_data)} users created with password '{DEFAULT_PASSWORD}'")

if __name__ == "__main__":
    populate_users()
