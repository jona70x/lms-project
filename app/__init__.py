from flask import Flask
from app.config import Config, db
from app.auth.routes import authentication_bp
from app.main.routes import main_bp
from app.assignments.routes import assignments_bp
"""For login functionality"""
from flask_login import LoginManager
from app.models import User, Course, Enrollment

login_manager = LoginManager()

create_app = Flask(__name__)
create_app.config.from_object(Config)

## Login manager 
db.init_app(create_app)
login_manager.init_app(create_app)
login_manager.login_view = "auth.login" # endpoint to visit
login_manager.login_message = "Please log in to access this page."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# registering main and auth routes
create_app.register_blueprint(authentication_bp, url_prefix = '/auth')
create_app.register_blueprint(main_bp, url_prefix = '/')
create_app.register_blueprint(assignments_bp, url_prefix = '/assignments')
