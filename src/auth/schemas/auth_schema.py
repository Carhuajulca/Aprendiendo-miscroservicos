from pydantic import BaseModel, EmailStr, Field

# src/auth/schemas/auth_schema.py
from pydantic import BaseModel, EmailStr

# Esquema de entrada (cuando el usuario inicia sesión)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Esquema de salida (cuando se genera un JWT)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    