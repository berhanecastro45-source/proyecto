from auxiliares.validaciones import es_administrador
import re
import bcrypt
from datetime import date
from peewee import IntegrityError

from datos.conexion import DB
from datos.repositorio.repo_usuario import (
    guardar_usuario,
    obtener_usuario_por_id,
    obtener_usuario_por_email,
    obtener_usuario_por_email_registrado,
    obtener_usuario_por_rut,
    obtener_usuario_por_rut_excluir,
    actualizar_usuario_repo,
    desactivar_usuario_repo,
    listado_usuario,
    listar_usuarios_inactivos,
    activar_usuario_repo
)
from datos.repositorio.repo_direccion import crear_direccion_repo


def normalizar_rut(rut):
    return rut.replace(".", "").replace("-", "").upper()


def validar_rut(rut):
    rut = str(rut).replace(".", "").replace("-", "").upper()

    if not re.fullmatch(r"\d{7,8}[0-9K]", rut):
        return False

    numero = rut[:-1]
    digito_verificador = rut[-1]

    suma = 0
    multiplicador = 2

    for digito in reversed(numero):
        suma += int(digito) * multiplicador

        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resultado = 11 - (suma % 11)

    if resultado == 11:
        resultado = "0"
    elif resultado == 10:
        resultado = "K"
    else:
        resultado = str(resultado)

    return digito_verificador == resultado


def validar_rut_disponible(rut):
    usuario = obtener_usuario_por_rut(rut)

    if usuario is not None:
        return False

    return True


def validar_password(password):
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")

    if not any(letra.isupper() for letra in password):
        raise ValueError("La contraseña debe tener una mayúscula.")

    if not any(letra.islower() for letra in password):
        raise ValueError("La contraseña debe tener una minúscula.")

    if not any(numero.isdigit() for numero in password):
        raise ValueError("La contraseña debe tener un número.")

    if not any(caracter in "@$!%*?&.#_-" for caracter in password):
        raise ValueError("La contraseña debe tener un carácter especial.")


def validar_datos_usuario(datos):
    if not validar_rut(datos["rut"]):
        raise ValueError("El RUT no es válido.")

    if not datos["nombre"] or len(datos["nombre"]) > 100:
        raise ValueError("El nombre no es válido.")

    if not datos["apellido_paterno"] or len(datos["apellido_paterno"]) > 100:
        raise ValueError("El apellido paterno no es válido.")

    if datos["apellido_materno"] and len(datos["apellido_materno"]) > 100:
        raise ValueError("El apellido materno es demasiado largo.")

    if "@" not in datos["email"] or len(datos["email"]) > 150:
        raise ValueError("El correo electrónico no es válido.")

    if datos["telefono"] and len(datos["telefono"]) > 20:
        raise ValueError("El teléfono es demasiado largo.")

    if not isinstance(datos["fecha_nacimiento"], date):
        raise ValueError("La fecha de nacimiento no es válida.")

    validar_password(datos["password"])


def validar_direccion(direccion):
    for campo in ("calle", "ciudad", "comuna", "region"):
        if not direccion.get(campo):
            raise ValueError("Debe completar todos los datos de la dirección.")

    if direccion.get("codigo_postal") and len(direccion["codigo_postal"]) > 20:
        raise ValueError("El código postal es demasiado largo.")


def listar_usuarios_negocio(usuario_actual):
    if not es_administrador(usuario_actual):
        raise PermissionError("No tienes permisos para listar usuarios.")

    return listado_usuario()


def obtener_usuario_para_actualizar_negocio(id_usuario, usuario_actual):
    if not es_administrador(usuario_actual):
        raise PermissionError("No tienes permisos para realizar esta acción.")

    usuario = obtener_usuario_por_id(id_usuario)

    if usuario is None or usuario.activo != 1:
        raise ValueError("El usuario no existe o está desactivado.")

    return usuario


def registrar_usuario_negocio(datos, direccion):
    validar_datos_usuario(datos)
    validar_direccion(direccion)

    datos["rut"] = normalizar_rut(datos["rut"])

    if obtener_usuario_por_email_registrado(datos["email"]):
        raise ValueError("El correo electrónico ya está registrado.")

    if obtener_usuario_por_rut(datos["rut"]):
        raise ValueError("El RUT ya está registrado.")

    password_hash = bcrypt.hashpw(
        datos["password"].encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        with DB.atomic():
            usuario = guardar_usuario(
                datos["rut"],
                datos["nombre"],
                datos["apellido_paterno"],
                datos["apellido_materno"],
                datos["email"],
                password_hash,
                datos["telefono"],
                datos["fecha_nacimiento"]
            )

            crear_direccion_repo(
                usuario.id_usuario,
                direccion["calle"],
                direccion["ciudad"],
                direccion["comuna"],
                direccion["region"],
                direccion["codigo_postal"]
            )

        return usuario

    except IntegrityError:
        raise ValueError("El RUT o correo electrónico ya se encuentra registrado.")


def actualizar_usuario_negocio(id_usuario, datos, usuario_actual):
    if not es_administrador(usuario_actual):
        raise PermissionError("No tienes permisos para modificar usuarios.")

    usuario = obtener_usuario_por_id(id_usuario)

    if usuario is None or usuario.activo != 1:
        raise ValueError("El usuario no existe o está desactivado.")

    datos["rut"] = normalizar_rut(datos["rut"])

    if not validar_rut(datos["rut"]):
        raise ValueError("El RUT no es válido.")

    if not datos["nombre"] or len(datos["nombre"]) > 100:
        raise ValueError("El nombre no es válido.")

    if not datos["apellido_paterno"] or len(datos["apellido_paterno"]) > 100:
        raise ValueError("El apellido paterno no es válido.")

    if datos["apellido_materno"] and len(datos["apellido_materno"]) > 100:
        raise ValueError("El apellido materno es demasiado largo.")

    if "@" not in datos["email"] or len(datos["email"]) > 150:
        raise ValueError("El correo electrónico no es válido.")

    if datos["telefono"] and len(datos["telefono"]) > 20:
        raise ValueError("El teléfono es demasiado largo.")

    otro_email = obtener_usuario_por_email_registrado(datos["email"])

    if otro_email and otro_email.id_usuario != id_usuario:
        raise ValueError("El correo electrónico ya está registrado.")

    otro_rut = obtener_usuario_por_rut_excluir(datos["rut"], id_usuario)

    if otro_rut:
        raise ValueError("El RUT ya está registrado.")

    try:
        return actualizar_usuario_repo(id_usuario, datos)

    except IntegrityError:
        raise ValueError("El RUT o correo electrónico ya está registrado.")


def desactivar_usuario_negocio(id_usuario, usuario_actual):
    if not es_administrador(usuario_actual):
        raise PermissionError("No tienes permisos para desactivar usuarios.")

    if id_usuario == usuario_actual.id_usuario:
        raise ValueError("No puedes desactivar tu propia cuenta.")

    usuario = obtener_usuario_por_id(id_usuario)

    if usuario is None or usuario.activo != 1:
        raise ValueError("El usuario no existe o ya está desactivado.")

    return desactivar_usuario_repo(id_usuario)


def login_usuario_negocio(email, password):
    usuario = obtener_usuario_por_email(email)

    if usuario is None:
        return None

    password_correcta = bcrypt.checkpw(
        password.encode("utf-8"),
        usuario.password_hash.encode("utf-8")
    )

    if not password_correcta:
        return None

    return usuario


def listar_usuarios_inactivos_negocio(usuario_actual):
    if not es_administrador(usuario_actual):
        raise PermissionError("No tienes permisos para administrar usuarios.")

    return listar_usuarios_inactivos()


def activar_usuario_negocio(id_usuario, usuario_actual):
    if not es_administrador(usuario_actual):
        raise PermissionError("No tienes permisos para administrar usuarios.")

    usuario = obtener_usuario_por_id(id_usuario)

    if usuario is None:
        raise ValueError("El usuario no existe.")

    if usuario.activo == 1:
        raise ValueError("El usuario ya se encuentra activo.")

    activar_usuario_repo(id_usuario)