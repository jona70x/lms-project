from flask import render_template, Blueprint, request, flash
from app.forms import LoginForm

authentication_bp = Blueprint("auth", __name__, template_folder='templates')

@authentication_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Rendering flash message with post
    if request.method == 'POST':
        form.validate()
        flash('Method not impleted, yet', 'warning')
        return render_template("auth/login.html", form=form)


    # Rendering from on get
    return render_template("auth/login.html", form=form)



