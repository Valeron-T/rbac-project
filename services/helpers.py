from datetime import datetime
import secrets
import string
from typing import List, Optional
from fastapi import Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from db import get_db
from models import AccessLog, Role, User
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
        request: Request,
        api_key: str = Depends(api_key_header),  # Extract API key from headers
        db: Session = Depends(get_db),
    ):
        """
        Validate API key and user access to the endpoint.
        """
        endpoint = request.url.path
        method = request.method
        # Validate API key
        user = db.query(User).filter_by(api_key=api_key).first()
        if not user:
            log_access(db, None, endpoint, method, success=False, message="Invalid API key")
            raise HTTPException(
                status_code=403,
                detail=ResponseSchema(
                    success=False, message="Invalid API key"
                ).model_dump(),
            )

        # Check user's role
        role: Role = user.role

        if role.name == "Admin" or "*" in allowed_roles:
            log_access(db, user.id, endpoint, method, success=True, message="")
            return user

        if role.name not in allowed_roles:
            log_access(db, user.id, endpoint, method, success=False, message="Insufficient privileges")
            raise HTTPException(
                status_code=403,
                detail=ResponseSchema(
                    success=False,
                    message=f"User with role '{role.name}' does NOT have access to this endpoint",
                ).model_dump(),
            )

        log_access(db, user.id, endpoint, method, success=True, message="")
        return user

    return access_dependency


def log_access(
    db: Session,
    user_id: Optional[str],
    endpoint: str,
    action: str,
    success: bool,
    message: Optional[str] = None,
):
    """
    Log access attempts to the database.
    """
    log_entry = AccessLog(
        user_id=user_id,
        endpoint=endpoint,
        action=action,
        success=success,
        message=message,
        timestamp=datetime.now(),
    )
    db.add(log_entry)
    db.commit()