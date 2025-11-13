
from sqlalchemy import Column, Integer, String, DateTime, func
from src.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    edad = Column(Integer, nullable=False)
    password_hash = Column(String(100), nullable=False)

    # Campos de auditoría
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    roles = relationship(
    "Role",
    secondary="users_roles",
    back_populates="users"
)