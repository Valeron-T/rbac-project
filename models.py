from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Table,
    create_engine,
    Enum as SQLAlchemyEnum,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from dotenv import load_dotenv
import os
from enum import Enum


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)  # Use Integer for ID
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

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
    role_id = Column(Integer, ForeignKey("roles.id"))  # Use Integer
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
