import pytest


def test_get_activities(client):
    """Test GET /activities returns activity data including a known activity."""
    # Arrange: No specific setup needed as activities are reset

    # Act: Make the GET request
    response = client.get("/activities")

    # Assert: Check status and content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success(client):
    """Test POST /activities/{activity_name}/signup successfully registers a participant."""
    # Arrange: Choose an activity and email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: Make the POST request
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check status and message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]


def test_signup_duplicate(client):
    """Test POST /activities/{activity_name}/signup returns 400 for duplicate signup."""
    # Arrange: First, sign up a student
    activity_name = "Programming Class"
    email = "test@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: Try to sign up the same student again
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check for 400 error
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_delete_participant_success(client):
    """Test DELETE /activities/{activity_name}/participants successfully removes a participant."""
    # Arrange: First, sign up a student
    activity_name = "Gym Class"
    email = "removeme@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: Delete the participant
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check status and message
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Removed {email} from {activity_name}" in data["message"]


def test_delete_participant_not_found(client):
    """Test DELETE /activities/{activity_name}/participants returns 404 for non-existent participant."""
    # Arrange: Choose an activity and non-existent email
    activity_name = "Art Workshop"
    email = "nonexistent@mergington.edu"

    # Act: Try to delete the non-existent participant
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check for 404 error
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Participant not found" in data["detail"]