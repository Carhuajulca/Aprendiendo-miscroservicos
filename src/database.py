from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from dotenv import load_dotenv
import os

# 🔹 Cargar variables de entorno
load_dotenv()

# 🔹 Obtener variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# 🔹 Puedes cambiar la URL a tu BD (MySQL, PostgreSQL, etc.)
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # más simple para comenzar


# 🔹 Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# 🔹 Crear la sesión (para interactuar con la BD)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Clase base de los modelos
Base = declarative_base()

# 🔹 Dependencia para obtener la sesión en los endpoints o servicios
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Manejo de transacciones automatico 
@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()