import os
import sys
import pytest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from app import create_app as flask_app 

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = flask_app
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


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
