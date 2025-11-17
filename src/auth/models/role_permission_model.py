# src/auth/models/role_permission_model.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from src.database import Base

roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)
