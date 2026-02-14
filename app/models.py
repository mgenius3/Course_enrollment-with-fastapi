from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class Role(str, Enum):
    student = "student"
    admin = "admin"

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    role: Role = Field(..., description="Role of the user (student or admin)")

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the course")
    code: str = Field(..., min_length=1, description="Unique code of the course")

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
