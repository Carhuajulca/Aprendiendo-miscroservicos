import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import Base, get_db

# 🔹 Base de datos temporal en memoria (no toca la real)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Crear las tablas una vez para todos los tests
Base.metadata.create_all(bind=engine)

# 🔹 Fixture para obtener la DB temporal
@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# 🔹 Fixture para el cliente de pruebas
@pytest.fixture()
def client(db_session):
    # Dependencia temporal para usar la DB de prueba
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# 📘 Qué hace este archivo:

# Crea una base de datos SQLite en memoria (no toca la original).

# Crea una sesión temporal (TestingSessionLocal).

# Usa dependency_overrides para reemplazar get_db() en FastAPI con la base de datos de prueba.

# Devuelve un TestClient(app) para hacer peticiones como si fueran reales (client.get, client.post, etc.).