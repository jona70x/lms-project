from flask import render_template, Blueprint


main_bp = Blueprint("main", __name__, template_folder='templates')

# root route
@main_bp.route('/')
def index():
    users = {'username' : 'Jonathan'}
    return render_template("/main/index.html", users=users)

