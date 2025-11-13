# src/auth/models/UserRoleModel.py
from sqlalchemy import Column, Integer, ForeignKey
from src.database import Base

# Para que un usuario pueda tener 1 o varios roles.
class UserRole(Base):
    __tablename__ = "users_roles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
