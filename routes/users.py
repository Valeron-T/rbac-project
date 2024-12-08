from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas import CreateUserRequest, GeneralResponseSchema, UserSchema, RoleSchema
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
    
    
    return GeneralResponseSchema(success=True,message="User created successfully",data={"id": db_user.id})


