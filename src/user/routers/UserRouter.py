
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.user.schemas.UserSchemas import UserCreate, UserResponse
from src.user.services.UserServices import UserService
from src.DataBase import get_db

user_router = APIRouter()
service = UserService()


#endpoint para lista usuarios
@user_router.get("/", response_model=list[UserResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return service.listar_usuarios(db)

# endpoint para con que te muestra un usuario por id
@user_router.get("/{usuario_id}", response_model=UserResponse)
def mostrar_usuario_por_id(usuario_id: int, db:Session=Depends(get_db)):
    return service.obtener_usuario_por_id(usuario_id,db)
    
#Endpoint para crear un usuario
@user_router.post("/", response_model=UserResponse)
def crear_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    return service.crear_usuario(usuario, db)

#Endpoint para actualizar un usuario
@user_router.put("/{usuario_id}", response_model=UserResponse)
def actualizar_usuario(user_id: int, usuario:UserCreate, db:Session = Depends(get_db)):
    return service.actualizar_usuario(user_id, usuario, db)

#Endpoint para eliminar un usuario
@user_router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(usuario_id:int, db:Session =Depends(get_db)):
    service.eliminar_usuairo(usuario_id,db)
    