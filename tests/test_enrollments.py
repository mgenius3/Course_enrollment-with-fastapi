def setup_data(client):
    # Create Student
    client.post("/users", json={"name": "Student", "email": "student@example.com", "role": "student"})
    # Create Admin
    client.post("/users", json={"name": "Admin", "email": "admin@example.com", "role": "admin"})
    # Create Course (as Admin)
    client.post("/courses", json={"title": "Math 101", "code": "MATH101"}, headers={"X-User-Role": "admin", "X-User-Id": "2"})
    
    return 1, 2, 1 # student_id, admin_id, course_id

def test_enroll_student(client):
    student_id, _, course_id = setup_data(client)
    headers = {"X-User-Role": "student", "X-User-Id": str(student_id)}
    
    response = client.post("/enrollments", json={"user_id": student_id, "course_id": course_id}, headers=headers)
    assert response.status_code == 201
    assert response.json()["user_id"] == student_id

def test_enroll_student_wrong_user(client):
    student_id, _, course_id = setup_data(client)
    headers = {"X-User-Role": "student", "X-User-Id": str(student_id)}
    
    # Student trying to enroll someone else (e.g. ID 99)
    response = client.post("/enrollments", json={"user_id": 99, "course_id": course_id}, headers=headers)
    assert response.status_code == 403

def test_enroll_twice(client):
    student_id, _, course_id = setup_data(client)
    headers = {"X-User-Role": "student", "X-User-Id": str(student_id)}
    
    client.post("/enrollments", json={"user_id": student_id, "course_id": course_id}, headers=headers)
    response = client.post("/enrollments", json={"user_id": student_id, "course_id": course_id}, headers=headers)
    assert response.status_code == 400
    assert "already enrolled" in response.json()["detail"]

def test_deregister_student(client):
    student_id, _, course_id = setup_data(client)
    headers = {"X-User-Role": "student", "X-User-Id": str(student_id)}
    
    enroll_res = client.post("/enrollments", json={"user_id": student_id, "course_id": course_id}, headers=headers)
    enrollment_id = enroll_res.json()["id"]
    
    response = client.delete(f"/enrollments/{enrollment_id}", headers=headers)
    assert response.status_code == 204

def test_admin_force_deregister(client):
    student_id, admin_id, course_id = setup_data(client)
    student_headers = {"X-User-Role": "student", "X-User-Id": str(student_id)}
    admin_headers = {"X-User-Role": "admin", "X-User-Id": str(admin_id)}
    
    enroll_res = client.post("/enrollments", json={"user_id": student_id, "course_id": course_id}, headers=student_headers)
    enrollment_id = enroll_res.json()["id"]
    
    response = client.delete(f"/enrollments/{enrollment_id}", headers=admin_headers)
    assert response.status_code == 204

def test_get_student_enrollments(client):
    student_id, _, course_id = setup_data(client)
    headers = {"X-User-Role": "student", "X-User-Id": str(student_id)}
    
    client.post("/enrollments", json={"user_id": student_id, "course_id": course_id}, headers=headers)
    
    response = client.get(f"/students/{student_id}/enrollments", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_admin_view_enrollments(client):
    student_id, admin_id, course_id = setup_data(client)
    student_headers = {"X-User-Role": "student", "X-User-Id": str(student_id)}
    admin_headers = {"X-User-Role": "admin", "X-User-Id": str(admin_id)}
    
    client.post("/enrollments", json={"user_id": student_id, "course_id": course_id}, headers=student_headers)
    
    response = client.get(f"/courses/{course_id}/enrollments", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_all_enrollments_admin(client):
    student_id, admin_id, course_id = setup_data(client)
    student_headers = {"X-User-Role": "student", "X-User-Id": str(student_id)}
    admin_headers = {"X-User-Role": "admin", "X-User-Id": str(admin_id)}
    
    client.post("/enrollments", json={"user_id": student_id, "course_id": course_id}, headers=student_headers)
    
    response = client.get("/enrollments", headers=admin_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
