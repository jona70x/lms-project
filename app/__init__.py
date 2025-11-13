from flask import Flask
from app.config import Config

create_app = Flask(__name__)
create_app.config.from_object(Config)

# Importing routes after creating the app instance
from app.main import routes as main_routes
from app.auth import routes as auth_routes
