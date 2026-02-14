# Project: Course Enrollment API (Beginner's Guide)

Welcome! This guide is designed to explain **everything** about this project from the ground up. Whether you are presenting this to a friend or just learning yourself, follow along to understand how a professional API is built.

---

## 1. What is this Project?

This is a **Course Enrollment System API**.

Think of it like the "brain" behind a university website. It doesn't have a visual interface (frontend), but it handles all the logic:
-   **Students** can sign up and enroll in classes.
-   **Admins** can create new courses and manage enrollments.
-   **Rules** are enforced (e.g., a student can't delete a course).

We built this using **FastAPI**, a modern and fast tool for building APIs in Python.

---

## 2. Key Concepts

### What is an API?
API stands for **Application Programming Interface**.
Imagine a restaurant:
-   **You (The Client)**: You sit at a table and look at the menu.
-   **The Kitchen (The Server)**: Where the food is made.
-   **The Waiter (The API)**: You tell the waiter what you want, and they bring your request to the kitchen and the food back to you.

In this project:
-   The **Client** is you (using Postman or Swagger UI).
-   The **Server** is this Python code running on your computer.
-   The **API** endpoints (like `/users` or `/courses`) are the "menu items" you can order.

### The "Database"
Usually, data is stored in a permanent database (like SQL).
For simplicity in this project, we use an **In-Memory Database**.
-   **What it means**: We use simple Python lists `[]` to store users and courses.
-   **Catch**: If you restart the server, the data disappears! This is perfect for learning and testing.

---

## 3. Project Structure (The Files)

Here is a tour of the project files and what they do:

### `requirements.txt`
This is the **Shopping List**. It tells Python which extra tools (libraries) we need to run the project.
-   `fastapi`: The web framework.
-   `uvicorn`: The server that runs the app.
-   `pydantic`: A tool to validate data (make sure an email looks like an email).

### `app/models.py`
This file defines the **Shapes of Data**.
We use classes called "Models" to define what a `User` or `Course` looks like.
-   **Example**: A `User` must have a `name` (string), `email` (string), and `role` ("student" or "admin").
-   **Why?**: If someone tries to create a user without an email, the API will automatically say "No!"

### `app/db.py`
This acts as our **Fake Database**.
It creates empty lists (`users = []`, `courses = []`) and provides helper functions to find items, like `get_user_by_email()`.

### `app/routers/`
These folders contain the **Logic** or "The Waiters".
-   `users.py`: Handles creating and finding users.
-   `courses.py`: Handles adding and viewing courses.
-   `enrollments.py`: Handles the complex logic of students signing up for classes.

### `app/main.py`
This is the **Entry Point**.
It brings everything together. It creates the `app` and includes all the routers so the server knows about them.

---

## 4. How to Run It (The Demo)

### Step 1: Start the Server
Open your terminal and run:
```bash
uvicorn app.main:app --reload
```
-   `uvicorn`: The program running the server.
-   `app.main:app`: Look in the `app` folder, `main.py` file, for the `app` object.
-   `--reload`: Restart the server automatically if we change code (great for development!).

### Step 2: Open the Interactive Docs
Go to your browser and visit:  
👉 **http://127.0.0.1:8000/docs**

This is the **Swagger UI**. It’s a magic page that FastAPI creates automatically. It lets you click buttons to test your API without writing code!

---

## 5. How We Test It (Quality Assurance)

We wrote automated tests to make sure the code works perfectly.
-   **Tool**: `pytest`
-   **Location**: `tests/` folder.

To run them, stop the server (Ctrl+C) and run:
```bash
python -m pytest
```
You should see **green dots** meaning all tests passed! This proves your logic (like preventing a student from deleting a course) works as expected.

---

## 6. How to Explain the "Role-Based Access"

This is the coolest part of the project!

1.  **Public Access**: Anyone can view courses (`GET /courses`).
2.  **Authentication Simulation**: Since we don't have a real login system, we "pretend" by sending **Headers** with our request.
    -   Header: `X-User-Role: admin` -> The API treats you as an Admin.
    -   Header: `X-User-Role: student` -> The API treats you as a Student.
3.  **The Logic**: In `courses.py`, we check:
    ```python
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admins only!")
    ```
    This simple check protects the entire system!

---

## Summary for Presentation

1.  **Introduction**: "I built a backend API for a course enrollment system."
2.  **Tech Stack**: "I used Python and FastAPI because it's fast and auto-generates documentation."
3.  **Features**: "It handles students, admins, courses, and enrollments with strict validation."
4.  **Demo**: Show them the Swagger UI (`/docs`) and create a user live.
5.  **Quality**: Run `pytest` to show 100% test passing rate.

Good luck with your presentation! 🚀
