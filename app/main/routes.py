from flask import render_template
from app import create_app

# root route
@create_app.route('/')
def home():
    users = {'username' : 'Jonathan'}
    return render_template("base.html", users=users)
