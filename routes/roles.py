from typing import List
from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session
from schemas import AssignPermissionToRoleSchema, GeneralResponseSchema
from models import Permission, Role
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


@router.post("/{role_id}/permissions")
def assign_permissions(
    role_id: str,
    payload: AssignPermissionToRoleSchema,
    db: Session = Depends(get_db),
    # _: bool = Depends(is_admin_user),  
):
    """Assign permissions to a role."""
    # Find the role
    role = db.query(Role).filter_by(id=role_id).first()
    if not role:
        return JSONResponse(
            status_code=404,
            content=GeneralResponseSchema(
                success=False,
                message="Role not found",
            ).model_dump(),
        )

    # Check if permissions exist
    permissions = (
        db.query(Permission).filter(Permission.id.in_(payload.permission_ids)).all()
    )
    if not permissions:
        return JSONResponse(
            status_code=404,
            content=GeneralResponseSchema(
                success=False,
                message="Some permissions not found",
            ).model_dump(),
        )

    # Filter out duplicate permissions
    existing_permission_ids = {perm.id for perm in role.permissions}
    new_permissions = [
        perm for perm in permissions if perm.id not in existing_permission_ids
    ]

    if not new_permissions:
        return GeneralResponseSchema(
            success=False,
            message="All permissions already exist for the role. No new permissions were added.",
        )

    # Add only new permissions to the role
    role.permissions.extend(new_permissions)
    db.commit()

    return GeneralResponseSchema(
        success=True,
        message=f"Added {len(new_permissions)} new permissions to role {role.name}.",
    )
