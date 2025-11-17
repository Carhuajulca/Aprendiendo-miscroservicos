from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.auth.services.auth_services import SECRET_KEY, ALGORITHM
from src.user.models.UserModel import User
from src.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o sin usuario"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )

    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return usuario

# =====================================================
#   VERIFICAR PERMISOS (RBAC)
# =====================================================
def require_permission(permission_name: str):
    """
    Dependencia para verificar si el usuario tiene un permiso específico.
    """

    def wrapper(current_user: User = Depends(obtener_usuario_actual)):

        # Extraer permisos del usuario
        user_permissions = {
            perm.name
            for role in (current_user.roles or [])
            for perm in (role.permissions or [])
        }

        if permission_name not in user_permissions:
            raise HTTPException(
                status_code=403,
                detail=f"No tienes el permiso requerido: {permission_name}"
            )

        return current_user  # 🔥 IMPORTANTE

    return wrapper


# El archivo dependency.py es un guardian de acceso.

# Este archivo se encarga de:

# 1️⃣ Recibir el token del cliente
# 2️⃣ Verificar si el token es válido
# 3️⃣ Verificar si no expiró
# 4️⃣ Leer el ID del usuario dentro del token
# 5️⃣ Buscar al usuario real en la base de datos
# 6️⃣ Retornar ese usuario
# 7️⃣ Bloquear acceso si algo falla