from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.services.auth_services import AuthService

auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Endpoint para autenticar al usuario y generar un token JWT.
    usuario = auth_service.autenticar_usuario(email=form_data.username, password=form_data.password, db=db)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.crear_token(usuario)
    
    return {"access_token": access_token, "token_type": "bearer"}
