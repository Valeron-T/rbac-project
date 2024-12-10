from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas import AssignPermissionToRoleSchema, GeneralResponseSchema, ResponseSchema
from models import Permission, Role
from db import get_db
from services.helpers import allow_access

router = APIRouter()


@router.get("/", response_model=GeneralResponseSchema)
def get_roles_list(db: Session = Depends(get_db)):
    """Retrieve a list of all roles."""
    roles = db.query(Role).all()
    return GeneralResponseSchema(
        success=True,
        message="Data fetched successfully",
        data={"result": [jsonable_encoder(role) for role in roles]},
    )



    
@router.get("/{role_id}/permissions", response_model=GeneralResponseSchema)
def list_permissions_for_role(role_id: str, db: Session = Depends(get_db)):
    """List permissions assigned to a specific role."""
    role = db.query(Role).filter_by(id=role_id).first()
    
    if not role:
        return JSONResponse(
            status_code=404,
            content=ResponseSchema(
                success=False,
                message="Role not found",
            ).model_dump(),
        )

    permissions = role.permissions  # This will load permissions related to the role (many-to-many relationship)
    
    return GeneralResponseSchema(
        success=True,
        message="Data fetched successfully",
        data={"result": [jsonable_encoder(permission) for permission in permissions]},
    )


@router.post("/{role_id}/permissions", dependencies=[Depends(allow_access())])
def assign_permissions(
    role_id: str,
    payload: AssignPermissionToRoleSchema,
    db: Session = Depends(get_db),
):
    """Assign permissions to a role."""
    # Find the role
    role = db.query(Role).filter_by(id=role_id).first()
    if not role:
        return JSONResponse(
            status_code=404,
            content=ResponseSchema(
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
            content=ResponseSchema(
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
        return ResponseSchema(
            success=False,
            message="All permissions already exist for the role. No new permissions were added.",
        )

    # Add only new permissions to the role
    role.permissions.extend(new_permissions)
    db.commit()

    return ResponseSchema(
        success=True,
        message=f"Added {len(new_permissions)} new permissions to role {str(role.name.value)}.",
    )
