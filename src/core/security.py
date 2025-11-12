# from passlib.context import CryptContext
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Configuramos el contexto de hashing con bcrypt
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

pwd_context = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    #Genera un hash seguro de una contraseña usando bcrypt.
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Verifica si una contraseña en texto plano coincide con el hash.
    try:
        pwd_context.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
            return False
    except Exception:
            return False
