from fastapi import HTTPException, status
from src.user.schemas.UserSchemas import UserCreate, UserResponse
from src.user.repositories.UserRepository import UserRepository
from sqlalchemy.orm import Session
from src.core.security import hash_password

class UserService:
    def __init__(self, repository: UserRepository = UserRepository()):
        self.repository =repository

    # Servicio para listar todos los usuairos    
    def listar_usuarios(self, db: Session):
        usuarios = self.repository.listar_usuarios(db)
        return [UserResponse.model_validate(u) for u in usuarios]
    
    # Servicio para obtener usuario por id
    def obtener_usuario_por_id(self,user_id:int, db:Session):
        usuario = self.repository.obtener_por_id(db,user_id)
        if not usuario:
            raise HTTPException(status_code=404, detail=f"Usuario de id: {user_id} no encontrado")
        return UserResponse.model_validate(usuario)
    
    # Servicio para crear usuario
    def crear_usuario(self, usuario:UserCreate, db: Session):
        existente = self.repository.obtener_por_email(db, usuario.email)
        if existente:
            raise HTTPException(status_code=400,detail=f"Email ya regitrado")
        usuario.password_hash = hash_password(usuario.password_hash)
        nuevo = self.repository.crear_usuario(db, usuario)
        return UserResponse.model_validate(nuevo)
    
    #Servicio para acutualizar
    def actualizar_usuario(self, user_id:int, datos: UserCreate, db:Session):
        usario = self.repository.obtener_por_id(db, user_id)
        if not usario:
            raise HTTPException(status_code=404, detail="usuario no encontrado")
        actualizado = self.repository.actualizar_usuario(db, usario, datos)
        return UserResponse.model_validate(actualizado)
    
    #Servicio para elimnar un usuario
    def eliminar_usuairo(self, usuario_id:int, db:Session):
        usuario = self.repository.obtener_por_id(db, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404,detail="id del usuario no entcontrado")
        return self.repository.eliminar_usuario(db, usuario)
