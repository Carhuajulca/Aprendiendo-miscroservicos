from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager


# 🔹 Puedes cambiar la URL a tu BD (MySQL, PostgreSQL, etc.)
DATABASE_URL = "postgresql://prueba:prueba123@localhost:5432/PRUEBA"  # más simple para comenzar


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