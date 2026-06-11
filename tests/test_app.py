def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_keys = {"Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Basketball Club", "Art Club", "Photography Club", "Debate Team", "Math Olympiad"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == expected_keys
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    get_response = client.get("/activities")
    participants = get_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_for_activity_rejects_duplicate_registration(client):
    # Arrange
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already registered for this activity"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    get_response = client.get("/activities")
    participants = get_response.json()[activity_name]["participants"]
    assert email not in participants


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Art Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
