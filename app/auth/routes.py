from flask import render_template
from app import create_app

# root route
@create_app.route('/auth/login')
def home():
    users = {'username' : 'Jonathan'}
    return render_template("login.html", users=users)
