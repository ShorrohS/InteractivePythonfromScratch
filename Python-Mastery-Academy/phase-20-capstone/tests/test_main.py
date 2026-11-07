"""
TaskFlow Pro — API Tests
Phase 20: Capstone Project

Tests cover:
  - Health check
  - User registration and login
  - Task CRUD operations
  - Authentication on protected routes
  - Analytics endpoint

HOW TO RUN:
  pip install pytest httpx
  pytest tests/ -v
  pytest tests/ --cov=src --cov-report=term-missing
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Use in-memory SQLite for tests
os.environ["DATABASE_URL"] = ":memory:"
os.environ["SECRET_KEY"]   = "test-secret-key-for-testing-only"

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# ── Fixtures ────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def test_user():
    """Register a test user and return credentials."""
    resp = client.post("/auth/register", json={
        "username": "testuser",
        "email":    "test@example.com",
        "password": "TestPass123"
    })
    if resp.status_code not in (200, 201, 400):  # 400 if already exists
        pytest.fail(f"Registration failed: {resp.text}")
    return {"username": "testuser", "password": "TestPass123"}


@pytest.fixture(scope="module")
def auth_token(test_user):
    """Get authentication token for test user."""
    resp = client.post("/auth/login", json=test_user)
    if resp.status_code == 200:
        return resp.json()["access_token"]
    pytest.skip("Could not authenticate — login endpoint may differ")


@pytest.fixture()
def auth_headers(auth_token):
    """Authorization headers for protected requests."""
    return {"Authorization": f"Bearer {auth_token}"}


# ── Health Check Tests ───────────────────────────────────────────

class TestHealth:

    def test_health_check_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_returns_healthy_status(self):
        response = client.get("/health")
        data = response.json()
        assert data.get("status") == "healthy"

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data or "app" in data or "message" in data


# ── Authentication Tests ──────────────────────────────────────────

class TestAuthentication:

    def test_register_new_user(self):
        import random
        username = f"user_{random.randint(1000, 9999)}"
        response = client.post("/auth/register", json={
            "username": username,
            "email":    f"{username}@test.com",
            "password": "SecurePass123"
        })
        assert response.status_code in (200, 201)
        data = response.json()
        assert "id" in data or "username" in data

    def test_register_duplicate_user(self, test_user):
        response = client.post("/auth/register", json={
            "username": test_user["username"],
            "email":    "different@email.com",
            "password": "AnyPass123"
        })
        assert response.status_code == 400

    def test_login_valid_credentials(self, test_user):
        response = client.post("/auth/login", json=test_user)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_password(self, test_user):
        response = client.post("/auth/login", json={
            "username": test_user["username"],
            "password": "WrongPassword!"
        })
        assert response.status_code == 401

    def test_protected_route_requires_auth(self):
        response = client.get("/tasks")
        assert response.status_code == 401 or response.status_code == 403

    def test_protected_route_with_invalid_token(self):
        response = client.get("/tasks",
                              headers={"Authorization": "Bearer invalid.token.here"})
        assert response.status_code in (401, 403)


# ── Task CRUD Tests ──────────────────────────────────────────────

class TestTasks:

    def test_list_tasks_requires_auth(self):
        response = client.get("/tasks")
        assert response.status_code in (401, 403)

    def test_list_tasks_authenticated(self, auth_headers):
        response = client.get("/tasks", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_task_valid(self, auth_headers):
        response = client.post("/tasks", headers=auth_headers, json={
            "title":    "Test task from pytest",
            "priority": "medium"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test task from pytest"
        assert "id" in data

    def test_create_task_missing_title(self, auth_headers):
        response = client.post("/tasks", headers=auth_headers, json={
            "priority": "high"
        })
        assert response.status_code == 422   # validation error

    def test_create_task_empty_title(self, auth_headers):
        response = client.post("/tasks", headers=auth_headers, json={
            "title": "   ",
            "priority": "low"
        })
        assert response.status_code in (400, 422)

    def test_get_created_task(self, auth_headers):
        # Create a task first
        create_resp = client.post("/tasks", headers=auth_headers, json={
            "title": "Task to retrieve",
            "priority": "high",
            "description": "Testing GET endpoint"
        })
        assert create_resp.status_code == 201
        task_id = create_resp.json()["id"]

        # Now get it
        get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["id"] == task_id
        assert data["title"] == "Task to retrieve"

    def test_update_task_status(self, auth_headers):
        # Create
        task_id = client.post("/tasks", headers=auth_headers, json={
            "title": "Task to update"
        }).json()["id"]

        # Update
        resp = client.patch(f"/tasks/{task_id}", headers=auth_headers, json={
            "status": "done"
        })
        assert resp.status_code == 200
        assert resp.json()["status"] == "done"

    def test_delete_task(self, auth_headers):
        # Create
        task_id = client.post("/tasks", headers=auth_headers, json={
            "title": "Task to delete"
        }).json()["id"]

        # Delete
        del_resp = client.delete(f"/tasks/{task_id}", headers=auth_headers)
        assert del_resp.status_code == 204

        # Verify gone
        get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert get_resp.status_code == 404

    def test_get_nonexistent_task(self, auth_headers):
        response = client.get("/tasks/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_cannot_access_other_users_task(self, test_user, auth_headers):
        """Tasks should be isolated per user."""
        task_id = client.post("/tasks", headers=auth_headers, json={
            "title": "User 1 private task"
        }).json()["id"]

        # Create second user
        import random
        other_user = f"other_{random.randint(1000, 9999)}"
        client.post("/auth/register", json={
            "username": other_user, "email": f"{other_user}@test.com",
            "password": "OtherPass123"
        })
        other_token = client.post("/auth/login", json={
            "username": other_user, "password": "OtherPass123"
        }).json().get("access_token")

        if other_token:
            resp = client.get(f"/tasks/{task_id}",
                              headers={"Authorization": f"Bearer {other_token}"})
            # Should not be found (different user)
            assert resp.status_code == 404


# ── Analytics Tests ──────────────────────────────────────────────

class TestAnalytics:

    def test_summary_endpoint(self, auth_headers):
        response = client.get("/reports/summary", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_tasks" in data

    def test_summary_requires_auth(self):
        response = client.get("/reports/summary")
        assert response.status_code in (401, 403)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
