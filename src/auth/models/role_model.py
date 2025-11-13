# src/auth/models/RoleModel.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base


# Cada rol es un "perfil" de acceso.
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    permissions = relationship(
        "Permission",
        secondary="roles_permissions",
        back_populates="roles"
    )

    users = relationship(
        "User",
        secondary="users_roles",
        back_populates="roles"
    )
