import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import db, InMemoryDB

@pytest.fixture(scope="function")
def client():
    # Reset DB before each test
    db.users = []
    db.courses = []
    db.enrollments = []
    return TestClient(app)

@pytest.fixture
def admin_headers():
    return {"X-User-Role": "admin", "X-User-Id": "1"}

@pytest.fixture
def student_headers():
    return {"X-User-Role": "student", "X-User-Id": "2"}
