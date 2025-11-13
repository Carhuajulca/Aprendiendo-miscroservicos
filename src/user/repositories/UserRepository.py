from sqlalchemy.orm import Session
from src.user.models.UserModel import User
from src.user.schemas.UserSchemas import UserCreate
from src.core.dependencies import obtener_usuario_actual


class UserRepository:

    #Repositorio para para obtener una lista de usuarios
    def listar_usuarios(self, db: Session):
        return db.query(User).all()
    
    # Repositorio para obtener un usuario por id
    def obtener_por_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    # Repositorio para obtener un usuario por email
    def obtener_por_email(self, db: Session, user_email: str):
        return db.query(User).filter(User.email == user_email).first()


    # Repositorio para crear un usuario
    def crear_usuario(self, db: Session, datos: UserCreate):
        nuevo = User(**datos.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    #Repositorio para actualizar un usuario
    def actualizar_usuario(self, db:Session, usuario:User, datos:UserCreate ):
        usuario.nombre = datos.nombre
        usuario.email = datos.email
        usuario.edad = datos.edad
        usuario.password_hash = datos.password_hash
        db.commit()
        db.refresh(usuario)
        return usuario
    

    def eliminar_usuario(self, db:Session, usuario: User):
        db.delete(usuario)
        db.commit()