from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas import GeneralResponseSchema
from models import Role
from db import get_db

router = APIRouter()


@router.get("/", response_model=GeneralResponseSchema)
def get_roles_list(db: Session = Depends(get_db)):
    """Retrieve a list of all roles."""
    # Query the users and join the Role table to get the role name
    roles = db.query(Role).all()
    # Return a list of user data with role name instead of role ID
    return GeneralResponseSchema(
        success=True,
        message="Data fetched successfully",
        data={"result": [jsonable_encoder(role) for role in roles]},
    )
