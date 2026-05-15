"""Tests for GET /activities endpoint"""
import pytest


class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all available activities"""
        # Arrange
        expected_activity_names = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Drama Club",
            "Debate Team",
            "Science Club",
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == len(expected_activity_names)
        for activity_name in expected_activity_names:
            assert activity_name in activities

    def test_get_activities_response_structure(self, client):
        """Test that each activity has the correct structure"""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict), f"{activity_name} is not a dict"
            for field in required_fields:
                assert field in activity_data, f"Field '{field}' missing from {activity_name}"
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_participants_are_emails(self, client):
        """Test that all participants are valid email strings"""
        # Arrange
        email_pattern = "@"

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert email_pattern in participant
