from pydantic import BaseModel
from enum import Enum
from typing import Any, List, Optional


# Define RoleEnum for serialization
class RoleEnum(str, Enum):
    STAFF = "Staff"
    SUPERVISOR = "Supervisor"
    ADMIN = "Admin"


class PermissionSchema(BaseModel):
    id: int
    name: str


class RoleSchema(BaseModel):
    id: int
    name: RoleEnum
    permissions: List[PermissionSchema]


class UserSchema(BaseModel):
    id: int
    username: str
    role: RoleEnum

    class Config:
        from_attributes = True


# Request schema for creating a user
class CreateUserRequest(BaseModel):
    username: str
    role: RoleEnum = RoleEnum.STAFF


class UpdateUserSchema(BaseModel):
    role: RoleEnum = RoleEnum.STAFF


class GeneralResponseSchema(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = (
        None  # Data can be any type, including lists, dictionaries, etc.
    )

    class Config:
        from_attributes = True
