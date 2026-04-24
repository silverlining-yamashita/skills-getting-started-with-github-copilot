from urllib.parse import quote

from src.app import activities


def test_get_activities_returns_all(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "anna@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "test@mergington.edu"
    path = f"/activities/{quote(activity_name)}/signup?email={quote(email)}"

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_removes_existing(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    path = f"/activities/{quote(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    path = f"/activities/{quote(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"


def test_remove_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "test@mergington.edu"
    path = f"/activities/{quote(activity_name)}/participants?email={quote(email)}"

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
