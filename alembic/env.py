# alembic/env.py (fragmento)
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import sys
import os

# Añadir la ruta raíz del proyecto al sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# alembic config
config = context.config
fileConfig(config.config_file_name)

# opción: leer DATABASE_URL desde el entorno
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# --- IMPORTA TUS MODELOS AQUÍ ---
# por ejemplo:
from src.DataBase import Base         # si usas SQLAlchemy declarative Base
from src.user.models.UserModel import User         # importa las clases de model
# o para SQLModel:
# from sqlmodel import SQLModel
# from myapp.models import *  # asegúrate de que MyModel está importado

target_metadata = Base.metadata  # o Base.metadata
# -----------------------------------

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
