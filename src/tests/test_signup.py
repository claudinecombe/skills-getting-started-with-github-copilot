"""Tests for POST /activities/{activity_name}/signup endpoint"""
import pytest


class TestSignupForActivity:
    def test_signup_valid_email_and_activity(self, client):
        """Test successful signup with valid email and activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_registration_returns_error(self, client):
        """Test that duplicate registration returns 400 error"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already" in data["detail"].lower()

    def test_signup_invalid_activity_returns_error(self, client):
        """Test that signup for non-existent activity returns 404 error"""
        # Arrange
        activity_name = "Non-Existent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_multiple_students_same_activity(self, client):
        """Test that multiple different students can sign up for the same activity"""
        # Arrange
        activity_name = "Chess Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"

        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_signup_adds_participant_to_activity(self, client):
        """Test that signup actually adds the participant to the activity"""
        # Arrange
        activity_name = "Programming Class"
        email = "verifyaddition@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity_name]["participants"]

    def test_signup_special_characters_in_email(self, client):
        """Test that signup works with special characters in email (URL encoding)"""
        # Arrange
        activity_name = "Tennis Club"
        email = "student+tag@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
