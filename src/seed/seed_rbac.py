from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.auth.models import Role, Permission
from src.auth.models import RolePermission
from src.user.models.UserModel import User
from src.core.security import hash_password

def run_seed():
    db: Session = SessionLocal()

    try:
        # -----------------------
        # 1. Crear Permisos
        # -----------------------
        permisos = [
            "ver_usuarios",
            "crear_usuarios",
            "editar_usuarios",
            "eliminar_usuarios",
            "ver_roles",
            "asignar_roles"
        ]

        permiso_objs = []
        for p in permisos:
            permiso = db.query(Permission).filter_by(name=p).first()
            if not permiso:
                permiso = Permission(name=p)
                db.add(permiso)
                permiso_objs.append(permiso)

        db.commit()

        # -----------------------
        # 2. Crear Roles
        # -----------------------
        roles = {
            "admin": permisos,        # admin tiene todos los permisos
            "moderador": ["ver_usuarios"],  
            "usuario": []             
        }

        for nombre_rol, permisos_lista in roles.items():
            rol = db.query(Role).filter_by(name=nombre_rol).first()
            if not rol:
                rol = Role(name=nombre_rol)
                db.add(rol)
                db.commit()

            # Asignar permisos al rol
            for nombre_permiso in permisos_lista:
                permiso = db.query(Permission).filter_by(name=nombre_permiso).first()

                existe = db.query(RolePermission).filter_by(
                    role_id=rol.id, 
                    permission_id=permiso.id
                ).first()

                if not existe:
                    rp = RolePermission(role_id=rol.id, permission_id=permiso.id)
                    db.add(rp)

        db.commit()

        # -----------------------
        # 3. Crear un usuario ADMIN
        # -----------------------
        admin = db.query(User).filter_by(email="admin@admin.com").first()
        if not admin:
            admin = User(
                nombre="Administrador",
                email="admin@admin.com",
                edad=30,
                password_hash=hash_password("123456")
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

            # asignarle rol admin
            rol_admin = db.query(Role).filter_by(name="admin").first()
            admin.roles.append(rol_admin)
            db.commit()

        print("✔ Datos RBAC pobiados correctamente")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
