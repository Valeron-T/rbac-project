from datetime import datetime
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
    api_key: str

    class Config:
        from_attributes = True
        

class UserResponseSchema(BaseModel):
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


class AssignPermissionToRoleSchema(BaseModel):
    permission_ids: List[str]


class ResponseSchema(BaseModel):
    success: bool
    message: str


class GeneralResponseSchema(ResponseSchema):
    data: Optional[Any] = None

    class Config:
        from_attributes = True


class AccessLogSchema(BaseModel):
    id: str
    user_id: Optional[str]
    endpoint: str
    action: str
    success: bool
    message: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class LogTimeRangeRequest(BaseModel):
    start_time: datetime
    end_time: datetime
