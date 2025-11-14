from flask import Flask
from app.config import Config
from app.auth.routes import authentication_bp

create_app = Flask(__name__)
create_app.config.from_object(Config)

# Importing routes after creating the app instance
from app.main import routes as main_routes


create_app.register_blueprint(authentication_bp, url_prefix = '/auth')
