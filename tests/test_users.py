def test_create_user(client):
    response = client.post("/users", json={"name": "Alice", "email": "alice@example.com", "role": "student"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data

def test_create_user_duplicate_email(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com", "role": "student"})
    response = client.post("/users", json={"name": "Bob", "email": "alice@example.com", "role": "admin"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_users(client):
    client.post("/users", json={"name": "Alice", "email": "alice@example.com", "role": "student"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_user_by_id(client):
    create_response = client.post("/users", json={"name": "Alice", "email": "alice@example.com", "role": "student"})
    user_id = create_response.json()["id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
