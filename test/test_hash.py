from src.core.security import hash_password, verify_password

hashed = hash_password("admin123")
print("Hash generado:", hashed)
print("Verificación:", verify_password("admin123", hashed))
