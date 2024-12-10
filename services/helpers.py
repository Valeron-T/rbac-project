import secrets
import string
from typing import List, Optional
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db import get_db
from models import Role, User
from fastapi.security import APIKeyHeader

from schemas import ResponseSchema

api_key_header = APIKeyHeader(name="Authorization")


def generate_api_key(length: int = 32) -> str:
    """Returns a cryptographically secure API key"""
    # Define the characters that can be used in the API key (uppercase, lowercase, digits, and special characters)
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a secure random API key
    api_key = "".join(secrets.choice(characters) for _ in range(length))
    return api_key


def allow_access(allowed_roles: Optional[List[str]] = []):
    def access_dependency(
        api_key: str = Depends(api_key_header),  # Extract API key from headers
        db: Session = Depends(get_db),
    ):
        """
        Validate API key and user access to the endpoint.
        """
        # Validate API key
        user = db.query(User).filter_by(api_key=api_key).first()
        if not user:
            raise HTTPException(
                status_code=403,
                detail=ResponseSchema(
                    success=False, message="Invalid API key"
                ).model_dump(),
            )

        # Check user's role
        role: Role = user.role

        if role.name == "Admin" or "*" in allowed_roles:
            return user

        if role.name not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=ResponseSchema(
                    success=False,
                    message=f"User with role '{role.name}' does NOT have access to this endpoint",
                ).model_dump(),
            )

        return user

    return access_dependency
