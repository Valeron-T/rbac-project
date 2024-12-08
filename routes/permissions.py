from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from schemas import GeneralResponseSchema
from models import Permission
from db import get_db

router = APIRouter()


@router.get("/", response_model=GeneralResponseSchema)
def get_permissions_list(db: Session = Depends(get_db)):
    """Retrieve a list of all permissions."""
    permissions = db.query(Permission).all()
    return GeneralResponseSchema(
        success=True,
        message="Data fetched successfully",
        data={"result": [jsonable_encoder(permission) for permission in permissions]},
    )

