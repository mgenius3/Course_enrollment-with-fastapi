def test_get_courses_empty(client):
    response = client.get("/courses")
    assert response.status_code == 200
    assert response.json() == []

def test_create_course_admin(client, admin_headers):
    response = client.post("/courses", json={"title": "Math 101", "code": "MATH101"}, headers=admin_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Math 101"

def test_create_course_student_forbidden(client, student_headers):
    response = client.post("/courses", json={"title": "History 101", "code": "HIST101"}, headers=student_headers)
    assert response.status_code == 403

def test_create_course_duplicate_code(client, admin_headers):
    client.post("/courses", json={"title": "Math 101", "code": "MATH101"}, headers=admin_headers)
    response = client.post("/courses", json={"title": "Math 102", "code": "MATH101"}, headers=admin_headers)
    assert response.status_code == 400

def test_update_course_admin(client, admin_headers):
    create_res = client.post("/courses", json={"title": "Math 101", "code": "MATH101"}, headers=admin_headers)
    course_id = create_res.json()["id"]
    
    response = client.put(f"/courses/{course_id}", json={"title": "Mathematics 101", "code": "MATH101-A"}, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Mathematics 101"

def test_delete_course_admin(client, admin_headers):
    create_res = client.post("/courses", json={"title": "Math 101", "code": "MATH101"}, headers=admin_headers)
    course_id = create_res.json()["id"]
    
    response = client.delete(f"/courses/{course_id}", headers=admin_headers)
    assert response.status_code == 204
    
    get_res = client.get(f"/courses/{course_id}")
    assert get_res.status_code == 404
