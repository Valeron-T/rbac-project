from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import APIKeyHeader
from db import get_db
from models import User

# Dependency to get API key from headers
api_key_header = APIKeyHeader(name="Authorization")


def get_user_by_api_key(api_key: str = Depends(api_key_header), db: Session = Depends(get_db)) -> User:
    """Query the database to find the user associated with the provided API key"""
    user = db.query(User).filter_by(api_key=api_key).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return user