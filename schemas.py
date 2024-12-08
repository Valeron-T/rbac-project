from enum import Enum
from pydantic import BaseModel


# Define a Role Enum to restrict roles to Staff, Supervisor, and Admin
class RoleEnum(str, Enum):
    STAFF = "Staff"
    SUPERVISOR = "Supervisor"
    ADMIN = "Admin"


class UserSchema(BaseModel):
    id: str
    username: str
    role: RoleEnum


class RoleSchema(BaseModel):
    id: str
    name: RoleEnum
    permissions: list[str]


class PermissionSchema(BaseModel):
    id: str
    name: str
