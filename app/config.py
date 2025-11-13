import os
from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


