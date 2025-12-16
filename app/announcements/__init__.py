from flask import Blueprint

announcements_bp = Blueprint("announcements", __name__, template_folder='templates')

# Import routes to register them with the blueprint
from app.announcements import routes
