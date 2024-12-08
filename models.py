from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Enum as SQLAlchemyEnum, create_engine
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
from enum import Enum


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)  # Use Integer for ID
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"


# Define the RoleEnum to limit role choices
class RoleEnum(str, Enum):
    STAFF = "Staff"
    SUPERVISOR = "Supervisor"
    ADMIN = "Admin"


# Association table for many-to-many relationships between Role and Permission
role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),  # Use Integer
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),  # Use Integer
)


class User(Base):
    __tablename__ = "users"
    username = Column(String(100), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")


class Role(Base):
    __tablename__ = "roles"
    name = Column(SQLAlchemyEnum(RoleEnum), unique=True, nullable=False)
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"
    name = Column(String(100), unique=True, nullable=False)
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")


if __name__ == "__main__":
    load_dotenv()
    
    # Create tables and establish the connection
    SQLALCHEMY_DATABASE_URL = os.getenv('DB_URL')
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Create tables in the database (only if they don't exist)
    Base.metadata.create_all(bind=engine)
