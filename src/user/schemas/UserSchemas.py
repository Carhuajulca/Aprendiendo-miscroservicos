from pydantic import BaseModel, EmailStr,ConfigDict
from pydantic import field_validator
from typing import Optional

class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    edad: int
    password_hash: str

    @field_validator("edad")
    def validar_edad(cls, v): # cls → es una referencia a la clase del modelo (como en los métodos de clase en Python).
        if v < 0:              # v → es el valor del campo que se está validando
            raise ValueError("La edad no puede ser negativo")
        return v

#Esquema para actualizar usuario
class Usuario_Actualizado(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    edad: Optional[int] = None
    password_hash: Optional[str] = None



class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    edad: int

    model_config = ConfigDict(from_attributes=True) 