"""Tests for DELETE /activities/{activity_name}/participants/{participant_email} endpoint"""
import pytest


class TestRemoveParticipant:
    def test_remove_participant_success(self, client):
        """Test successful removal of a participant"""
        # Arrange
        activity_name = "Art Studio"
        email = "isabella@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_participant_not_found(self, client):
        """Test removing non-existent participant returns 404 error"""
        # Arrange
        activity_name = "Drama Club"
        email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_participant_invalid_activity(self, client):
        """Test removing participant from non-existent activity returns 404"""
        # Arrange
        activity_name = "Non-Existent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_participant_actually_removes_from_list(self, client):
        """Test that participant is actually removed from the activity"""
        # Arrange
        activity_name = "Debate Team"
        email = "marcus@mergington.edu"

        # Act
        client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email not in activities[activity_name]["participants"]

    def test_remove_participant_does_not_affect_other_activities(self, client):
        """Test that removing participant from one activity doesn't affect others"""
        # Arrange
        participant_email = "hannah@mergington.edu"
        activity_to_remove_from = "Science Club"
        other_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Get initial state
        initial_response = client.get("/activities")
        initial_activities = initial_response.json()

        # Act
        client.delete(
            f"/activities/{activity_to_remove_from}/participants/{participant_email}"
        )
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert participant_email not in activities[activity_to_remove_from]["participants"]
        for activity_name in other_activities:
            if participant_email in initial_activities[activity_name]["participants"]:
                assert participant_email in activities[activity_name]["participants"]

    def test_remove_participant_special_characters_in_email(self, client):
        """Test removal with special characters in email (URL encoding)"""
        # Arrange
        activity_name = "Basketball Team"
        special_email = "special+tag@mergington.edu"

        # First add the participant
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": special_email}
        )

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{special_email}"
        )

        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert special_email not in activities[activity_name]["participants"]

    def test_remove_multiple_participants(self, client):
        """Test that multiple participants can be removed from same activity"""
        # Arrange
        activity_name = "Chess Club"
        email1 = "removetest1@mergington.edu"
        email2 = "removetest2@mergington.edu"

        # Add both participants
        client.post(f"/activities/{activity_name}/signup", params={"email": email1})
        client.post(f"/activities/{activity_name}/signup", params={"email": email2})

        # Act
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{email1}"
        )
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{email2}"
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 not in activities[activity_name]["participants"]
        assert email2 not in activities[activity_name]["participants"]
