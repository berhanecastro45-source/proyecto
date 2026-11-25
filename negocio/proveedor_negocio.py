from auxiliares.validaciones import validar_administrador
from peewee import IntegrityError

from datos.repositorio.repo_proveedor import (
    listar_proveedores_repo,
    listar_proveedores_desactivados_repo,
    obtener_proveedor_por_id_repo,
    obtener_proveedor_desactivado_por_id_repo,
    obtener_proveedor_por_rut_repo,
    obtener_proveedor_por_email_repo,
    crear_proveedor_repo,
    actualizar_proveedor_repo,
    eliminar_proveedor_repo,
    reactivar_proveedor_repo
)


def validar_id(id_proveedor):
    if isinstance(id_proveedor, bool) or not isinstance(id_proveedor, int) or id_proveedor <= 0:
        raise ValueError("El ID debe ser un número entero positivo.")


def validar_rut(rut):
    if not isinstance(rut, str) or not rut.strip():
        raise ValueError("El RUT del proveedor es obligatorio.")

    rut = rut.strip().upper().replace(".", "").replace("-", "")

    if len(rut) < 2 or len(rut) > 9:
        raise ValueError("El RUT ingresado no tiene un formato válido.")

    numero = rut[:-1]
    digito = rut[-1]

    if not numero.isdigit() or not (digito.isdigit() or digito == "K"):
        raise ValueError("El RUT ingresado no tiene un formato válido.")

    suma = 0
    multiplicador = 2

    for numero_actual in reversed(numero):
        suma += int(numero_actual) * multiplicador
        multiplicador += 1

        if multiplicador > 7:
            multiplicador = 2

    resultado = 11 - (suma % 11)

    if resultado == 11:
        digito_calculado = "0"
    elif resultado == 10:
        digito_calculado = "K"
    else:
        digito_calculado = str(resultado)

    if digito != digito_calculado:
        raise ValueError("El dígito verificador del RUT es incorrecto.")

    return numero + "-" + digito


def validar_nombre(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre del proveedor es obligatorio.")

    nombre = nombre.strip()

    if len(nombre) > 100:
        raise ValueError("El nombre no puede superar los 100 caracteres.")

    if nombre.isdigit():
        raise ValueError("El nombre no puede contener solamente números.")

    return nombre


def validar_telefono(telefono):
    if telefono is None or (isinstance(telefono, str) and not telefono.strip()):
        return None

    if not isinstance(telefono, str):
        raise ValueError("El teléfono debe ser texto.")

    telefono = telefono.strip()

    if len(telefono) > 20:
        raise ValueError("El teléfono no puede superar los 20 caracteres.")

    if not any(caracter.isdigit() for caracter in telefono):
        raise ValueError("El teléfono debe contener números.")

    for caracter in telefono:
        if not (caracter.isdigit() or caracter in " +-()"):
            raise ValueError("El teléfono contiene caracteres no permitidos.")

    return telefono


def validar_email(email):
    if not isinstance(email, str):
        raise ValueError("Ingrese un correo electrónico válido.")

    email = email.strip()

    if len(email) > 150:
        raise ValueError("El correo no puede superar los 150 caracteres.")

    if email.count("@") != 1:
        raise ValueError("Ingrese un correo electrónico válido.")

    partes = email.split("@")
    usuario = partes[0]
    dominio = partes[1]

    if not usuario or not dominio or "." not in dominio:
        raise ValueError("Ingrese un correo electrónico válido.")

    if dominio.startswith(".") or dominio.endswith("."):
        raise ValueError("Ingrese un correo electrónico válido.")

    if " " in email:
        raise ValueError("El correo no puede contener espacios.")

    return email


def listar_proveedores_negocio():
    return listar_proveedores_repo()


def listar_proveedores_desactivados_negocio(rol):
    validar_administrador(rol)
    return listar_proveedores_desactivados_repo()


def buscar_proveedor_negocio(id_proveedor):
    validar_id(id_proveedor)

    proveedor = obtener_proveedor_por_id_repo(id_proveedor)

    if proveedor is None:
        raise ValueError("No se encontró el proveedor solicitado.")

    return proveedor


def crear_proveedor_negocio(rut, nombre, telefono, email, rol):
    validar_administrador(rol)

    rut = validar_rut(rut)
    nombre = validar_nombre(nombre)
    telefono = validar_telefono(telefono)
    email = validar_email(email)

    proveedor_rut = obtener_proveedor_por_rut_repo(rut)
    proveedor_email = obtener_proveedor_por_email_repo(email)

    if proveedor_rut is not None:
        if proveedor_rut.activo == 0:
            raise ValueError("Este RUT pertenece a un proveedor desactivado. Puedes reactivarlo desde el menú.")
        raise ValueError("Ya existe un proveedor con ese RUT.")

    if proveedor_email is not None:
        if proveedor_email.activo == 0:
            raise ValueError("Este correo pertenece a un proveedor desactivado. Puedes reactivarlo desde el menú.")
        raise ValueError("Ya existe un proveedor con ese correo electrónico.")

    try:
        return crear_proveedor_repo(rut, nombre, telefono, email)

    except IntegrityError:
        raise ValueError("El RUT o correo electrónico ya está registrado.")


def actualizar_proveedor_negocio(id_proveedor, rut, nombre, telefono, email, rol):
    validar_administrador(rol)
    validar_id(id_proveedor)

    rut = validar_rut(rut)
    nombre = validar_nombre(nombre)
    telefono = validar_telefono(telefono)
    email = validar_email(email)

    proveedor = obtener_proveedor_por_id_repo(id_proveedor)

    if proveedor is None:
        raise ValueError("No se encontró el proveedor que deseas modificar.")

    proveedor_rut = obtener_proveedor_por_rut_repo(rut)
    proveedor_email = obtener_proveedor_por_email_repo(email)

    if proveedor_rut is not None and proveedor_rut.id_proveedor != id_proveedor:
        raise ValueError("Ya existe otro proveedor con ese RUT.")

    if proveedor_email is not None and proveedor_email.id_proveedor != id_proveedor:
        raise ValueError("Ya existe otro proveedor con ese correo electrónico.")

    try:
        resultado = actualizar_proveedor_repo(
            id_proveedor, rut, nombre, telefono, email
        )

        if not resultado:
            raise ValueError("No se pudo actualizar el proveedor.")

        return True

    except IntegrityError:
        raise ValueError("El RUT o correo electrónico ya está registrado.")


def eliminar_proveedor_negocio(id_proveedor, rol):
    validar_administrador(rol)
    validar_id(id_proveedor)

    proveedor = obtener_proveedor_por_id_repo(id_proveedor)

    if proveedor is None:
        raise ValueError("No se encontró el proveedor que deseas desactivar.")

    resultado = eliminar_proveedor_repo(id_proveedor)

    if not resultado:
        raise ValueError("No se pudo desactivar el proveedor.")

    return True


def reactivar_proveedor_negocio(id_proveedor, rol):
    validar_administrador(rol)
    validar_id(id_proveedor)

    proveedor = obtener_proveedor_desactivado_por_id_repo(id_proveedor)

    if proveedor is None:
        raise ValueError("No se encontró un proveedor desactivado con ese ID.")

    resultado = reactivar_proveedor_repo(id_proveedor)

    if not resultado:
        raise ValueError("No se pudo reactivar el proveedor.")

    return True
