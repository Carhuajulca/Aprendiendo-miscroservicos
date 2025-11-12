from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# Revision identifiers
revision: str = '8a7e8b592632'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1️⃣ Agregar nuevas columnas (password_hash y auditoría)
    op.add_column('users', sa.Column('password_hash', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))

    # 2️⃣ Copiar los valores antiguos de "password" a "password_hash"
    users_table = table('users',
                        column('password', sa.String),
                        column('password_hash', sa.String))
    op.execute(users_table.update().values(password_hash=users_table.c.password))

    # 3️⃣ Eliminar la columna antigua
    op.drop_column('users', 'password')

    # 4️⃣ Hacer que password_hash no permita nulos (ya tiene datos copiados)
    op.alter_column('users', 'password_hash', nullable=False)


def downgrade() -> None:
    # Revertir los cambios
    op.add_column('users', sa.Column('password', sa.String(length=100), nullable=False))
    op.execute("UPDATE users SET password = password_hash")
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'password_hash')
