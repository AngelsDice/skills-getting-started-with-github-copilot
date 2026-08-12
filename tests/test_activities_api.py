from urllib.parse import quote


def test_get_activities_returns_activity_catalog(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]
    assert "michael@mergington.edu" in payload["Chess Club"]["participants"]


def test_signup_success_adds_email_to_activity(client):
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    updated = client.get("/activities").json()
    assert email in updated[activity]["participants"]


def test_signup_rejects_duplicate_student(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown%20Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_removes_student_from_activity(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{quote(activity)}/participants/{quote(email)}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

    updated = client.get("/activities").json()
    assert email not in updated[activity]["participants"]


def test_unregister_missing_participant_returns_404(client):
    activity = "Chess Club"
    email = "notregistered@mergington.edu"

    response = client.delete(f"/activities/{quote(activity)}/participants/{quote(email)}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"
