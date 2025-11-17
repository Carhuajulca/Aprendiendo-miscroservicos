# src/auth/models/user_role_model.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from src.database import Base

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)
