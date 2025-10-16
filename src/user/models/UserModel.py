from sqlalchemy import Column, Integer, String
from src.DataBase import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    edad = Column(Integer, nullable=False)
    password  = Column(String(100), nullable=False)
