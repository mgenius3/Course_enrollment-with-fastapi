from fastapi import APIRouter, HTTPException, Path, Header, Depends
from typing import List, Optional
from app.models import Course, CourseCreate, Role
from app.db import db

router = APIRouter()

def get_current_user_role(x_user_role: str = Header(..., description="Role of the user making the request")):
    # In a real app, we would verify the token. Here we just trust the header as per instructions.
    return x_user_role

@router.get("/courses", response_model=List[Course], summary="Retrieve all courses")
def get_courses():
    """
    Public access: Retrieve a list of all available courses.
    """
    return db.courses

@router.get("/courses/{course_id}", response_model=Course, summary="Retrieve a course by ID")
def get_course(course_id: int = Path(..., title="The ID of the course to get")):
    """
    Public access: Retrieve details of a specific course.
    """
    course = db.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/courses", response_model=Course, status_code=201, summary="Create a new course (Admin only)")
def create_course(
    course: CourseCreate, 
    role: str = Depends(get_current_user_role)
):
    """
    Admin only: Create a new course.
    """
    if role != Role.admin:
        raise HTTPException(status_code=403, detail="Operation not permitted. Admins only.")
    
    if db.get_course_by_code(course.code):
        raise HTTPException(status_code=400, detail="Course code must be unique")
    
    new_course_id = len(db.courses) + 1
    new_course = Course(id=new_course_id, **course.dict())
    db.courses.append(new_course)
    return new_course

@router.put("/courses/{course_id}", response_model=Course, summary="Update a course (Admin only)")
def update_course(
    course_data: CourseCreate,
    course_id: int = Path(..., title="The ID of the course to update"),
    role: str = Depends(get_current_user_role)
):
    """
    Admin only: Update an existing course.
    """
    if role != Role.admin:
        raise HTTPException(status_code=403, detail="Operation not permitted. Admins only.")
        
    course = db.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check uniqueness of code if changed
    existing_course_with_code = db.get_course_by_code(course_data.code)
    if existing_course_with_code and existing_course_with_code.id != course_id:
        raise HTTPException(status_code=400, detail="Course code must be unique")

    course.title = course_data.title
    course.code = course_data.code
    return course

@router.delete("/courses/{course_id}", status_code=204, summary="Delete a course (Admin only)")
def delete_course(
    course_id: int = Path(..., title="The ID of the course to delete"),
    role: str = Depends(get_current_user_role)
):
    """
    Admin only: Delete a course.
    """
    if role != Role.admin:
        raise HTTPException(status_code=403, detail="Operation not permitted. Admins only.")
    
    course = db.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.courses.remove(course)
    # Cascade delete enrollments? Not explicitly required but good practice.
    # Requirement says "Deregistration must fail if the enrollment does not exist", but doesn't specify cascade.
    # I'll leave it simple for now, or just remove enrollments to keep DB clean.
    db.enrollments = [e for e in db.enrollments if e.course_id != course_id]
    
    return
