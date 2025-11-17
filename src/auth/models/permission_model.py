# src/auth/models/permission_model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base
from src.auth.models.role_permission_model import roles_permissions

# Representa cada acción permitida.
class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # ej: "ventas.crear"
    description = Column(String(255))

    roles = relationship(
        "Role",
        secondary=roles_permissions,
        back_populates="permissions"
    )
