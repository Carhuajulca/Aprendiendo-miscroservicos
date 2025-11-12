# src/auth/services/auth_service.py
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
from src.core.security import verify_password
from src.user.models.UserModel import User
from sqlalchemy.orm import Session
from src.auth.schemas.auth_schema import TokenResponse
from src.user.repositories.UserRepository import UserRepository
from dotenv import load_dotenv
import os

# ==========================
# CONFIGURACIÓN DEL TOKEN
# ==========================

SECRET_KEY = os.getenv("SECRET_KEY")  # 👈 clave secreta
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # duración del token

class AuthService:
    def __init__(self,repository: UserRepository = UserRepository()):
        self.repository = repository

    # Servicio encargado de autenticar usuarios y generar tokens JWT
    def autenticar_usuario(self, email: str, password: str, db: Session):
        """Verifica que el usuario exista y la contraseña sea válida"""
        usuario = self.repository.obtener_por_email(db, email)
        # usuario = db.query(User).filter(User.email == email).first()

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        if not verify_password(password, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña incorrecta"
            )

        return usuario

    def crear_token(self, usuario: User) -> TokenResponse:
        """Genera un token JWT para un usuario autenticado"""
        data = {
            "sub": str(usuario.id),
            "email": usuario.email,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        return TokenResponse(access_token=token, token_type="bearer")

    def verificar_token(self, token: str):
        """Verifica si un token es válido y no ha expirado"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado"
            )


# Recordatorio: Para verificar un usuario lo haremos por medio del correo electrónico 