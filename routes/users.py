from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas import (
    CreateUserRequest,
    GeneralResponseSchema,
    UpdateUserSchema,
    UserSchema,
    RoleSchema,
)
from models import User, Role
from db import get_db

router = APIRouter()


@router.post("/", status_code=201, response_model=GeneralResponseSchema)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    """Create a new user."""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    role = db.query(Role).filter(Role.name == user.role).first()

    if not role:
        raise Exception("Role not found")

    db_user = User(username=user.username, role_id=role.id)

    db.add(db_user)
    db.commit()

    # Refresh to get ID
    db.refresh(db_user)

    return GeneralResponseSchema(
        success=True,
        message="User created successfully",
        data={"id": db_user.id, "name": db_user.username, "role": db_user.role.name},
    )


@router.get("/", response_model=GeneralResponseSchema)
def get_user_list(db: Session = Depends(get_db)):
    """Retrieve a list of all users."""
    # Query the users and join the Role table to get the role name
    users = db.query(User).join(Role).all()

    # Return a list of user data with role name instead of role ID
    return GeneralResponseSchema(
        success=True,
        message="Data fetched successfully",
        data={
            "result": [
                jsonable_encoder(
                    UserSchema(id=user.id, username=user.username, role=user.role.name)
                )
                for user in users
            ]
        },
    )


@router.get("/{user_id}", response_model=GeneralResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a user."""
    # Query the users and join the Role table to get the role name
    users = db.query(User).filter(User.id == user_id).join(Role).all()

    # Return a list of user data with role name instead of role ID
    return GeneralResponseSchema(
        success=True,
        message="Data fetched successfully",
        data={
            "result": [
                jsonable_encoder(
                    UserSchema(id=user.id, username=user.username, role=user.role.name)
                )
                for user in users
            ]
        },
    )


@router.put("/{user_id}/role/", response_model=GeneralResponseSchema)
def assign_role(user_id: int, payload: UpdateUserSchema, db: Session = Depends(get_db)):
    """Assign a predefined role to a user."""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role_obj = db.query(Role).filter(Role.name == payload.role).first()
    if not role_obj:
        raise HTTPException(status_code=404, detail="Role not found")

    user.role_id = role_obj.id
    db.commit()
    db.refresh(user)
    return GeneralResponseSchema(
        success=True,
        message="User role updated successfully",
        data={
            "result": [
                jsonable_encoder(
                    UserSchema(id=user.id, username=user.username, role=user.role.name)
                )
            ]
        },
    )
