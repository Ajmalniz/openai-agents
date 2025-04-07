import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the DACA Analytics Service! Access /docs for the API documentation."
    }

def test_get_analytics():
    # Test for existing user
    response = client.get("/analytics/alice")
    assert response.status_code == 200
    assert response.json() == {"message_count": 5}

    # Test for another existing user
    response = client.get("/analytics/bob")
    assert response.status_code == 200
    assert response.json() == {"message_count": 3}

    # Test for non-existing user
    response = client.get("/analytics/charlie")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}