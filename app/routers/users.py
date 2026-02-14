from fastapi import APIRouter, HTTPException, Path, Body
from typing import List
from app.models import User, UserCreate, Role
from app.db import db
from pydantic import EmailStr

router = APIRouter()

@router.post("/users", response_model=User, status_code=201, summary="Create a new user")
def create_user(user: UserCreate):
    """
    Create a new user with the following information:
    - **name**: Name of the user
    - **email**: Email address of the user
    - **role**: Role of the user (student or admin)
    """
    if db.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user_id = len(db.users) + 1
    new_user = User(id=new_user_id, **user.dict())
    db.users.append(new_user)
    return new_user

@router.get("/users", response_model=List[User], summary="Retrieve all users")
def get_users():
    """
    Retrieve a list of all registered users.
    """
    return db.users

@router.get("/users/{user_id}", response_model=User, summary="Retrieve a user by ID")
def get_user(user_id: int = Path(..., title="The ID of the user to get")):
    """
    Retrieve a specific user by their ID.
    """
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
