import pytest
from fastapi.testclient import TestClient
from app.main import app

pytestmark = [pytest.mark.integration]

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "balance": 100.0
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["balance"] == 100.0
    assert "id" in data

def test_get_users():
    client.post("/users", json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "balance": 50.0
    })
    
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1

def test_transfer_money():
    user1 = client.post("/users", json={
        "name": "Alice",
        "email": "alice@example.com",
        "balance": 100.0
    }).json()
    
    user2 = client.post("/users", json={
        "name": "Bob",
        "email": "bob@example.com",
        "balance": 50.0
    }).json()
    
    response = client.post("/transfer", json={
        "from_user_id": user1["id"],
        "to_user_id": user2["id"],
        "amount": 25.0
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["from_user"]["balance"] == 75.0
    assert data["to_user"]["balance"] == 75.0

def test_duplicate_email():
    client.post("/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "balance": 100.0
    })
    
    response = client.post("/users", json={
        "name": "Another User",
        "email": "test@example.com",
        "balance": 50.0
    })
    
    assert response.status_code == 409