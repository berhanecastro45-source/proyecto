from auxiliares.validaciones import validar_administrador
from peewee import IntegrityError

from datos.repositorio.repo_forma_pago import (
    listar_formas_pago_repo,
    listar_formas_pago_desactivadas_repo,
    obtener_forma_pago_por_id_repo,
    obtener_forma_pago_desactivada_por_id_repo,
    obtener_forma_pago_por_nombre_repo,
    crear_forma_pago_repo,
    actualizar_forma_pago_repo,
    desactivar_forma_pago_repo,
    reactivar_forma_pago_repo
)


def validar_id(id_forma_pago):
    if isinstance(id_forma_pago, bool) or not isinstance(id_forma_pago, int):
        raise ValueError(
            "El ID de la forma de pago debe ser un número entero."
        )

    if id_forma_pago <= 0:
        raise ValueError(
            "El ID de la forma de pago debe ser positivo."
        )


def validar_nombre(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError(
            "El nombre de la forma de pago es obligatorio."
        )

    nombre = nombre.strip()

    if len(nombre) > 100:
        raise ValueError(
            "El nombre de la forma de pago no puede superar los 100 caracteres."
        )

    return nombre


def validar_descripcion(descripcion):
    if not isinstance(descripcion, str) or not descripcion.strip():
        raise ValueError(
            "La descripción de la forma de pago es obligatoria."
        )

    descripcion = descripcion.strip()

    if len(descripcion) > 255:
        raise ValueError(
            "La descripción no puede superar los 255 caracteres."
        )

    return descripcion


def listar_formas_pago_negocio():
    return listar_formas_pago_repo()


def listar_formas_pago_desactivadas_negocio(rol):
    validar_administrador(rol)
    return listar_formas_pago_desactivadas_repo()


def obtener_forma_pago_negocio(id_forma_pago):
    validar_id(id_forma_pago)

    forma_pago = obtener_forma_pago_por_id_repo(id_forma_pago)

    if forma_pago is None:
        raise ValueError(
            "No se encontró la forma de pago solicitada."
        )

    return forma_pago


def crear_forma_pago_negocio(nombre, descripcion, rol):
    validar_administrador(rol)

    nombre = validar_nombre(nombre)
    descripcion = validar_descripcion(descripcion)

    forma_existente = obtener_forma_pago_por_nombre_repo(nombre)

    if forma_existente:
        if forma_existente.activo == 0:
            raise ValueError(
                "Esta forma de pago está desactivada. Puedes reactivarla desde el menú."
            )

        raise ValueError(
            "Ya existe una forma de pago con ese nombre."
        )

    try:
        return crear_forma_pago_repo(nombre, descripcion)

    except IntegrityError:
        raise ValueError(
            "Ese nombre ya está registrado."
        )


def actualizar_forma_pago_negocio(
    id_forma_pago,
    nombre,
    descripcion,
    rol
):
    validar_administrador(rol)
    validar_id(id_forma_pago)

    nombre = validar_nombre(nombre)
    descripcion = validar_descripcion(descripcion)

    forma_pago = obtener_forma_pago_por_id_repo(id_forma_pago)

    if forma_pago is None:
        raise ValueError(
            "No se encontró la forma de pago que deseas modificar."
        )

    forma_existente = obtener_forma_pago_por_nombre_repo(nombre)

    if (
        forma_existente
        and forma_existente.id_forma_pago != id_forma_pago
    ):
        raise ValueError(
            "Ya existe otra forma de pago con ese nombre."
        )

    try:
        resultado = actualizar_forma_pago_repo(
            id_forma_pago,
            nombre,
            descripcion
        )

        if not resultado:
            raise ValueError(
                "No se pudo actualizar la forma de pago."
            )

        return True

    except IntegrityError:
        raise ValueError(
            "No se pudo actualizar porque ese nombre ya está registrado."
        )


def desactivar_forma_pago_negocio(id_forma_pago, rol):
    validar_administrador(rol)
    validar_id(id_forma_pago)

    forma_pago = obtener_forma_pago_por_id_repo(id_forma_pago)

    if forma_pago is None:
        raise ValueError(
            "No se encontró la forma de pago que deseas desactivar."
        )

    resultado = desactivar_forma_pago_repo(id_forma_pago)

    if not resultado:
        raise ValueError(
            "No se pudo desactivar la forma de pago."
        )

    return True


def reactivar_forma_pago_negocio(id_forma_pago, rol):
    validar_administrador(rol)
    validar_id(id_forma_pago)

    forma_pago = obtener_forma_pago_desactivada_por_id_repo(
        id_forma_pago
    )

    if forma_pago is None:
        raise ValueError(
            "No se encontró una forma de pago desactivada con ese ID."
        )

    resultado = reactivar_forma_pago_repo(id_forma_pago)

    if not resultado:
        raise ValueError(
            "No se pudo reactivar la forma de pago."
        )

    return True


