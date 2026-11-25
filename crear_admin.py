"""Crea el usuario administrador inicial (ejecutar una sola vez).

Uso:  python crear_admin.py
Requiere la base de datos importada y el archivo .env configurado.
"""
import bcrypt

from datos.conexion import DB
from datos.modelos.usuario import Usuario

EMAIL = "admin@tienda.cl"
PASSWORD = "Admin.2026"


def crear_admin():
    DB.connect()

    try:
        if Usuario.get_or_none(Usuario.email == EMAIL) is not None:
            print("El administrador ya existe.")
            return

        password_hash = bcrypt.hashpw(
            PASSWORD.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        admin = Usuario(
            rut="111111111",
            nombre="Admin",
            apellido_paterno="Sistema",
            email=EMAIL,
            password_hash=password_hash,
            rol="ADMINISTRADOR",
            activo=1
        )
        admin.save()

        print(f"Administrador creado: {EMAIL} / {PASSWORD}")
    finally:
        DB.close()


if __name__ == "__main__":
    crear_admin()
