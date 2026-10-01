import pytest
from app import create_app
from app.db import get_db

@pytest.fixture()
def app(tmp_path):
    app = create_app({"TESTING": True, "SECRET_KEY": "test-secret", "DATABASE_PATH": str(tmp_path / "test.sqlite3"), "DEFAULT_ADMIN_USERNAME": "rootadmin", "DEFAULT_ADMIN_PASSWORD": "RootAdmin123!"})
    yield app

@pytest.fixture()
def client(app):
    client = app.test_client()
    client.get("/")
    return client

def token(client):
    with client.session_transaction() as session:
        return session["csrf_token"]

def test_home_and_seeded_admin_login(client):
    assert client.get("/").status_code == 200
    response = client.post("/login", data={"csrf_token": token(client), "username": "rootadmin", "password": "RootAdmin123!"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Enrollment overview" in response.data

def test_student_signup_and_application(client, app):
    response = client.post("/signup", data={"csrf_token": token(client), "first_name": "Ana", "last_name": "Santos", "email": "ana@example.com", "username": "ana", "password": "Password123!"}, follow_redirects=True)
    assert b"Account created" in response.data
    response = client.post("/login", data={"csrf_token": token(client), "username": "ana", "password": "Password123!"}, follow_redirects=True)
    assert b"Student dashboard" in response.data
    response = client.post("/student/apply", data={"csrf_token": token(client), "program": "Bachelor of Science in Information Technology", "school_year": "2026-2027", "notes": "Ready"}, follow_redirects=True)
    assert b"Enrollment application submitted" in response.data
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM applications").fetchone()[0] == 1

def test_rbac_blocks_student_from_admin(client):
    client.post("/signup", data={"csrf_token": token(client), "first_name": "A", "last_name": "B", "email": "a@b.com", "username": "student", "password": "Password123!"})
    client.post("/login", data={"csrf_token": token(client), "username": "student", "password": "Password123!"})
    assert client.get("/admin/dashboard").status_code == 403
