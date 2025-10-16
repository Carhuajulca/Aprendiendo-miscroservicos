from sqlalchemy.orm import Session
from src.user.models.UserModel import User
from src.user.schemas.UserSchemas import UserCreate
from src.DataBase import session_scope

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

    # Repositorio para crear un nuevo usuario
    # def crear_usuario(self, db: Session, usuario: UserCreate):
    #     # usar con try/except para evitar errores en caso de duplicados de email o fallo en la base de datos.
    #     try:
    #         nuevo_usuario = User(
    #             nombre=usuario.nombre,
    #             email=usuario.email,
    #             edad=usuario.edad,
    #             password=usuario.password
    #         )
    #         db.add(nuevo_usuario)
    #         db.commit()
    #         db.refresh(nuevo_usuario)
    #         return nuevo_usuario
    #     except Exception as e:
    #         db.rollback()
    #         raise e

    def crear_usuario(self, datos: UserCreate):
        with session_scope() as db:
            nuevo = User(**datos.model_dump())
            db.add(nuevo)
            db.commit()          # 👈 Guarda realmente en la base de datos
            db.refresh(nuevo)    # 👈 Actualiza el objeto con los datos guardados
            return nuevo

    #Repositorio para actualizar un usuario
    def actualizar_usuario(self, db:Session, usuario:User, datos:UserCreate ):
        usuario.nombre = datos.nombre
        usuario.email = datos.email
        usuario.password = datos.password
        db.commit()
        db.refresh(usuario)
        return usuario
    

    def eliminar_usuario(self, db:Session, usuario: User):
        db.delete(usuario)
        db.commit()