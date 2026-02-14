from fastapi import FastAPI
from app.routers import users, courses, enrollments

app = FastAPI(
    title="Course Enrollment Management API",
    description="API for managing students, courses, and enrollments with role-based access control.",
    version="1.0.0"
)

app.include_router(users.router, tags=["Users"])
app.include_router(courses.router, tags=["Courses"])
app.include_router(enrollments.router, tags=["Enrollments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Course Enrollment Management API"}