from flask import Flask
from app.config import Config
from app.auth.routes import authentication_bp
from app.main.routes import main_bp

create_app = Flask(__name__)
create_app.config.from_object(Config)

# registering main and auth routes
create_app.register_blueprint(authentication_bp, url_prefix = '/auth')
create_app.register_blueprint(main_bp, url_prefix = '/')
