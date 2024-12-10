from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import (
    CreateUserRequest,
    GeneralResponseSchema,
    ResponseSchema,
    UpdateUserSchema,
    UserResponseSchema,
    UserSchema,
)
from models import User, Role
from db import get_db
from services.helpers import generate_api_key

router = APIRouter()


@router.post("/", status_code=201)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    """Create a new user."""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=ResponseSchema(
                success=False, message="User already exists"
            ).model_dump(),
        )

    role = db.query(Role).filter(Role.name == user.role).first()

    if not role:
        raise HTTPException(
            status_code=400,
            detail=ResponseSchema(success=False, message="Invalid Role").model_dump(),
        )

    db_user = User(username=user.username, role_id=role.id, api_key=generate_api_key())

    db.add(db_user)
    db.commit()

    # Refresh to get ID
    db.refresh(db_user)

    return GeneralResponseSchema(
        success=True,
        message="User created successfully",
        data=UserSchema(
            id=db_user.id,
            username=db_user.username,
            role=db_user.role.name,
            api_key=db_user.api_key,
        ).model_dump(),
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
                UserResponseSchema(
                    id=user.id,
                    username=user.username,
                    role=user.role.name,
                ).model_dump()
                for user in users
            ]
        },
    )


@router.get("/{user_id}", response_model=GeneralResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a user."""
    # Query the users and join the Role table to get the role name
    user = db.query(User).filter(User.id == user_id).join(Role).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail=ResponseSchema(success=False, message="User not found").model_dump(),
        )

    # Return a list of user data with role name instead of role ID
    return GeneralResponseSchema(
        success=True,
        message="Data fetched successfully",
        data={
            "result": UserResponseSchema(
                id=user.id,
                username=user.username,
                role=user.role.name,
            ).model_dump()
        },
    )


@router.put("/{user_id}/role/", response_model=GeneralResponseSchema)
def assign_role(user_id: int, payload: UpdateUserSchema, db: Session = Depends(get_db)):
    """Assign a predefined role to a user."""

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail=ResponseSchema(success=False, message="User not found").model_dump(),
        )

    role_obj = db.query(Role).filter(Role.name == payload.role).first()
    if not role_obj:
        raise HTTPException(
            status_code=400,
            detail=ResponseSchema(success=False, message="Role not found").model_dump(),
        )

    user.role_id = role_obj.id
    db.commit()
    db.refresh(user)
    return GeneralResponseSchema(
        success=True,
        message="User role updated successfully",
        data={
            "result": [
                UserResponseSchema(
                    id=user.id,
                    username=user.username,
                    role=user.role.name,
                ).model_dump()
            ]
        },
    )
