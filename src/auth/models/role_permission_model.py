# src/auth/models/RolePermissionModel.py
from sqlalchemy import Column, Integer, ForeignKey
from src.database import Base


# Relaciona M:N → un rol tiene muchos permisos, un permiso pertenece a muchos roles.
class RolePermission(Base):
    __tablename__ = "roles_permissions"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)
