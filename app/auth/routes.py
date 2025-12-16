from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.config import db
from app.forms import LoginForm, RegistrationForm
from urllib.parse import urlparse, urljoin

authentication_bp = Blueprint("auth", __name__, template_folder='templates')

# handling user registration
@authentication_bp.route('/register', methods=['GET', 'POST'])
def register():
    # If already logged in, redirect home
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        # new user
        user = User(email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)

        # saving to db
        db.session.add(user)
        db.session.commit()

        # if success display message
        flash('Registration successful!, Please login in', 'success')

        return redirect(url_for('auth.login'))
    
    # Display form validation errors if they exist
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'danger')
    
    return render_template('auth/register.html', form=form)
    


def is_safe_url(target):
    # validates redirect URL to prevent open redirects
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # check if user exist and password matches
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username of password', 'danger')
            return redirect(url_for('auth.login'))
        # log in user
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get("next")
        if next_page and is_safe_url(next_page):
            return redirect(next_page)
        else:
            return redirect(next_page or url_for("main.index"))

    return render_template("auth/login.html", form=form)


@authentication_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for("main.index"))
