# Course Enrollment Management API

A RESTful API built with FastAPI for managing students, courses, and enrollments. This project demonstrates role-based access control, data validation, and relationship management using an in-memory database.

## Features

- **User Management**: Create and retrieve users (Students and Admins).
- **Course Management**: Publicly view courses; Admins can create, update, and delete courses.
- **Enrollment Management**: Students can enroll/deregister; Admins can oversee all enrollments.
- **Role-Based Access Control**: Strict permissions for Student vs Admin operations.
- **In-Memory Storage**: Uses Python lists to simulate a database.

## Setup & Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.
2.  **Create a virtual environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the API

Start the server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

- **Swagger UI**: Visit `http://127.0.0.1:8000/docs` to explore the API interactively.
- **ReDoc**: Visit `http://127.0.0.1:8000/redoc` for alternative documentation.

## Running Tests

This project includes a comprehensive test suite using `pytest`.

To run the tests:

```bash
python -m pytest
```

Ensure all 19+ tests pass to verify the system's integrity.

## API Usage & Roles

The API uses **Headers** to simulate authentication and role verification.

- **Admin Access**:
    - Header: `X-User-Role: admin`
    - Header: `X-User-Id: 1` (or any valid admin ID)
- **Student Access**:
    - Header: `X-User-Role: student`
    - Header: `X-User-Id: 2` (or your valid student ID)

### Example Requests

**Create a Course (Admin)**
`POST /courses`
Headers: `X-User-Role: admin`
Body:
```json
{
  "title": "Intro to FastAPI",
  "code": "CS101"
}
```

**Enroll in a Course (Student)**
`POST /enrollments`
Headers: `X-User-Role: student`, `X-User-Id: 2`
Body:
```json
{
  "user_id": 2,
  "course_id": 1
}
```

## Project Structure

- `app/main.py`: Entry point of the application.
- `app/models.py`: Pydantic models for data validation.
- `app/db.py`: In-memory database simulation.
- `app/routers/`: Separate files for Users, Courses, and Enrollments logic.
- `tests/`: Automated tests for all valid and invalid scenarios.

---
**Note**: This is an educational project focusing on API design and testing. Data is lost when the server restarts.
