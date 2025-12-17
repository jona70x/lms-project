from flask import Flask
from flask_login import LoginManager, current_user
from app.config import Config, db
from app.auth.routes import authentication_bp
from app.main.routes import main_bp
from app.assignments.routes import assignments_bp
from app.courses import courses_bp
from app.announcements import announcements_bp
"""For login functionality"""
from flask_login import LoginManager
from app.models import User, Course, Enrollment, Assignment, StudentAssignment, Announcement
from flask_login import current_user
from flask import render_template

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # blueprints
    app.register_blueprint(authentication_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)  # <-- no prefix, so "/" works
    app.register_blueprint(assignments_bp, url_prefix="/assignments")
    app.register_blueprint(courses_bp, url_prefix="/courses")

    # Notifications available to all templates
    @app.context_processor
    def inject_notifications():
        if current_user.is_authenticated:
            notifications = (Notification.query
                .filter_by(user_id=current_user.id, is_read=False)
                .order_by(Notification.created_at.desc())
                .limit(5)
                .all()
            )
            return dict(notifications=notifications)
        return dict(notifications=[])

    return app
# registering main and auth routes
create_app.register_blueprint(authentication_bp, url_prefix = '/auth')
create_app.register_blueprint(main_bp, url_prefix = '/')
create_app.register_blueprint(assignments_bp, url_prefix = '/assignments')
create_app.register_blueprint(courses_bp, url_prefix = '/courses')
create_app.register_blueprint(announcements_bp, url_prefix = '/announcements')

# fallback route for app
@create_app.errorhandler(404)
def page_not_found(error):
    return render_template('coming_soon.html'), 404
