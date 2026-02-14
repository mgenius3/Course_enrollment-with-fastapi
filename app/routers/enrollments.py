from fastapi import APIRouter, HTTPException, Path, Header, Depends, Query
from typing import List, Optional
from app.models import Enrollment, EnrollmentCreate, Role
from app.db import db

router = APIRouter()

def get_current_user_info(
    x_user_role: str = Header(..., description="Role of the requester"),
    x_user_id: int = Header(..., description="ID of the requester")
):
    return {"role": x_user_role, "id": x_user_id}

@router.post("/enrollments", response_model=Enrollment, status_code=201, summary="Enroll a student within a course")
def enroll_student(
    enrollment: EnrollmentCreate,
    user_info: dict = Depends(get_current_user_info)
):
    """
    Student only: Enroll in a course.
    """
    requester_role = user_info["role"]
    requester_id = user_info["id"]

    if requester_role != Role.student:
        raise HTTPException(status_code=403, detail="Only students can enroll in courses")
    
    # improved security: ensure student is enrolling themselves
    if enrollment.user_id != requester_id:
         raise HTTPException(status_code=403, detail="You can only enroll yourself")

    if not db.get_user(enrollment.user_id):
        raise HTTPException(status_code=404, detail="Student not found")
    
    if not db.get_course(enrollment.course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    
    if db.is_enrolled(enrollment.user_id, enrollment.course_id):
         raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    new_enrollment_id = len(db.enrollments) + 1
    new_enrollment = Enrollment(id=new_enrollment_id, **enrollment.dict())
    db.enrollments.append(new_enrollment)
    return new_enrollment

@router.delete("/enrollments/{enrollment_id}", status_code=204, summary="Deregister from a course")
def deregister_student(
    enrollment_id: int = Path(..., title="The ID of the enrollment to remove"),
    user_info: dict = Depends(get_current_user_info)
):
    """
    Student: Deregister themselves.
    Admin: Force deregister.
    """
    requester_role = user_info["role"]
    requester_id = user_info["id"]
    
    enrollment = db.get_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    if requester_role == Role.student:
        if enrollment.user_id != requester_id:
             raise HTTPException(status_code=403, detail="You can only deregister your own enrollments")
    elif requester_role == Role.admin:
        pass # Admin can delete any enrollment
    else:
         raise HTTPException(status_code=403, detail="Operation not permitted")

    db.enrollments.remove(enrollment)
    return

@router.get("/students/{student_id}/enrollments", response_model=List[Enrollment], summary="Retrieve enrollments for a specific student")
def get_student_enrollments(
    student_id: int = Path(..., title="The ID of the student"),
    user_info: dict = Depends(get_current_user_info)
):
    """
    Retrieve enrollments for a specific student.
    """
    requester_role = user_info["role"]
    requester_id = user_info["id"]

    # Access control: Student can view own, Admin can view all
    if requester_role == Role.student and requester_id != student_id:
        raise HTTPException(status_code=403, detail="You can only view your own enrollments")
    
    if not db.get_user(student_id):
        raise HTTPException(status_code=404, detail="Student not found")
        
    return db.get_student_enrollments(student_id)

@router.get("/enrollments", response_model=List[Enrollment], summary="Retrieve all enrollments (Admin only)")
def get_all_enrollments(
    user_info: dict = Depends(get_current_user_info)
):
    """
    Admin only: Retrieve all enrollments.
    """
    if user_info["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Operation not permitted. Admins only.")
    
    return db.enrollments

@router.get("/courses/{course_id}/enrollments", response_model=List[Enrollment], summary="Retrieve enrollments for a specific course (Admin only)")
def get_course_enrollments(
    course_id: int = Path(..., title="The ID of the course"),
    user_info: dict = Depends(get_current_user_info)
):
    """
    Admin only: Retrieve enrollments for a specific course.
    """
    if user_info["role"] != Role.admin:
        raise HTTPException(status_code=403, detail="Operation not permitted. Admins only.")
    
    if not db.get_course(course_id):
        raise HTTPException(status_code=404, detail="Course not found")

    return db.get_course_enrollments(course_id)
