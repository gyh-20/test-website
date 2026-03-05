"""
Backend API Test Suite
Tests all endpoints of the login/registration application
"""
import requests
import pytest

BASE_URL = "http://localhost:5000"


class TestBackendAPI:
    """Test suite for backend API endpoints"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Clean up users before each test"""
        requests.post(f"{BASE_URL}/reset_users")

    def test_1_unregistered_user_login(self):
        """Scenario 1: Unregistered user attempts login"""
        response = requests.post(
            f"{BASE_URL}/login",
            json={"username": "nonexistent", "password": "anypass"}
        )
        data = response.json()

        assert response.status_code == 401
        assert data["success"] is False
        assert data["message"] == "User not found"

    def test_2_register_new_user(self):
        """Scenario 4: Register new user successfully"""
        # First try - should succeed
        response = requests.post(
            f"{BASE_URL}/register",
            json={"username": "testuser", "password": "testpass123"}
        )
        data = response.json()

        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Registration successful"

    def test_3_login_with_correct_credentials(self):
        """Scenario 2: Registered user logs in with correct credentials"""
        # Register user first
        requests.post(
            f"{BASE_URL}/register",
            json={"username": "testuser", "password": "testpass123"}
        )

        # Now login
        response = requests.post(
            f"{BASE_URL}/login",
            json={"username": "testuser", "password": "testpass123"}
        )
        data = response.json()

        assert response.status_code == 200
        assert data["success"] is True
        assert data["message"] == "Login successful"
        assert data["username"] == "testuser"

    def test_4_login_with_incorrect_password(self):
        """Scenario 3: Registered user logs in with incorrect password"""
        # Register user first
        requests.post(
            f"{BASE_URL}/register",
            json={"username": "testuser", "password": "testpass123"}
        )

        # Try login with wrong password
        response = requests.post(
            f"{BASE_URL}/login",
            json={"username": "testuser", "password": "wrongpass"}
        )
        data = response.json()

        assert response.status_code == 401
        assert data["success"] is False
        assert data["message"] == "Incorrect password"

    def test_5_register_existing_username(self):
        """Scenario 5: Register with existing username"""
        # Register user first time
        requests.post(
            f"{BASE_URL}/register",
            json={"username": "existinguser", "password": "pass123"}
        )

        # Try to register again with same username
        response = requests.post(
            f"{BASE_URL}/register",
            json={"username": "existinguser", "password": "anotherpass"}
        )
        data = response.json()

        assert response.status_code == 409
        assert data["success"] is False
        assert data["message"] == "Username already exists"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
