from fastapi import FastAPI
from src.user.routers.UserRouter import  user_router
from src.DataBase import Base, engine

# Crear las tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi Proyecto FastAPI")

app.include_router(user_router, prefix="/api/v1/user", tags=["Users"])

@app.get("/")
async def root():
    """
    Endpoint raíz de la API.
    
    Returns:
        dict: Mensaje de bienvenida
    """
    return {
        "message": "¡Hola, FastAPI!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }