import os
import sys
import pytest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from app import create_app as flask_app

try:
    from app.extensions import db
except ImportError:
    from app import db


@pytest.fixture
def client():
    app = flask_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.session.remove()
        db.drop_all()



def test_index_page(client):
    """Home page should load with status code 200."""
    resp = client.get("/")
    assert resp.status_code == 200


def test_login_page(client):
    """Login page should load."""
    resp = client.get("/auth/login")
    assert resp.status_code == 200


def test_gpa_requires_login(client):
    """GPA page should redirect when not logged in."""
    resp = client.get("/gpa", follow_redirects=False)
    assert resp.status_code in (301, 302)


def test_assignments_requires_login(client):
    """Assignments page should also redirect when not logged in."""
    resp = client.get("/courses/1/assignments", follow_redirects=False)
    assert resp.status_code in (301, 302)

# ---------- route tests (logged out) ----------

@pytest.mark.parametrize("path", [
    "/",                          # main.index
    "/auth/login",                # auth.login
    "/auth/register",             # auth.register

    "/dashboard",                 # main.dashboard
    "/gpa",                       # main.gpa_calculator
    "/messages",                  # main.messages
    "/messages/1",                # main.message_detail

    "/courses/",                  # courses.courses_list
    "/courses/my-courses",        # courses.my_courses
    "/courses/my-created-courses",# courses.my_created_courses
    "/courses/1",                 # courses.course_detail
    "/courses/1/dashboard",       # courses.course_dashboard
    "/courses/1/dashboard/overview",  # courses.course_dashboard with tab

    "/courses/1/assignments",     # main.assignments_list
    "/assignments/",              # assignments.index
    "/assignments/1",             # assignments.assignment_detail
    "/assignments/1/submissions", # assignments.assignment_submissions
])
def test_get_routes_do_not_500(client, path):
    resp = client.get(path, follow_redirects=False)
    assert resp.status_code < 500


# ---------- POST route tests (logged out) ----------

@pytest.mark.parametrize("path", [
    "/courses/new",                           # courses.create_course
    "/courses/1/update",                      # courses.update_course
    "/courses/1/delete",                      # courses.delete_course
    "/courses/1/enroll",                      # courses.enroll_course
    "/courses/1/drop",                        # courses.drop_course
    "/courses/1/assignment/1/toggle-status",  # courses.toggle_assignment_status

    "/assignments/new",                       # assignments.create_assignment
    "/assignments/new/1",                     # assignments.create_assignment w course_id
    "/assignments/1/edit",                    # assignments.update_assignment
    "/assignments/1/update",                  # assignments.update_assignment
    "/assignments/1/delete",                  # assignments.delete_assignment
    "/assignments/1/grade/1",                 # assignments.grade_submission

    "/announcements/new",                     # announcements.create_announcement
    "/announcements/new/1",                   # announcements.create_announcement w course_id
    "/announcements/1/update",                # announcements.update_announcement
    "/announcements/1/delete",                # announcements.delete_announcement
])
def test_post_routes_do_not_500(client, path):
    resp = client.post(path, data={}, follow_redirects=False)
    assert resp.status_code < 500
