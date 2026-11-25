from auxiliares.validaciones import validar_administrador

from peewee import IntegrityError

from datos.repositorio.repo_marca import (
    obtener_marcas_repo,
    obtener_marcas_desactivadas_repo,
    obtener_marca_por_id_repo,
    obtener_marca_desactivada_por_id_repo,
    obtener_marca_por_nombre_repo,
    crear_marca_repo,
    actualizar_marca_repo,
    eliminar_marca_repo,
    reactivar_marca_repo
)


def validar_id(id_marca):
    if isinstance(id_marca, bool) or not isinstance(id_marca, int):
        raise ValueError("El ID de la marca debe ser un número entero.")

    if id_marca <= 0:
        raise ValueError("El ID de la marca debe ser positivo.")


def validar_nombre(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre de la marca es obligatorio.")

    nombre = nombre.strip()

    if len(nombre) > 100:
        raise ValueError(
            "El nombre de la marca no puede superar los 100 caracteres."
        )

    if nombre.isdigit():
        raise ValueError(
            "El nombre de la marca no puede contener solamente números."
        )

    return nombre


def listar_marcas_negocio():
    return obtener_marcas_repo()


def listar_marcas_desactivadas_negocio(rol):
    validar_administrador(rol)
    return obtener_marcas_desactivadas_repo()


def buscar_marca_negocio(id_marca):
    validar_id(id_marca)

    marca = obtener_marca_por_id_repo(id_marca)

    if marca is None:
        raise ValueError("No se encontró la marca solicitada.")

    return marca


def crear_marca_negocio(nombre, rol):
    validar_administrador(rol)
    nombre = validar_nombre(nombre)

    marca = obtener_marca_por_nombre_repo(nombre)

    if marca:
        if marca.activo == 0:
            raise ValueError(
                "Esta marca está desactivada. Puedes reactivarla desde el menú."
            )

        raise ValueError("Ya existe una marca con ese nombre.")

    try:
        return crear_marca_repo(nombre)

    except IntegrityError:
        raise ValueError("Ese nombre ya está registrado.")


def actualizar_marca_negocio(id_marca, nombre, rol):
    validar_administrador(rol)
    validar_id(id_marca)
    nombre = validar_nombre(nombre)

    marca = obtener_marca_por_id_repo(id_marca)

    if marca is None:
        raise ValueError(
            "No se encontró la marca que deseas modificar."
        )

    marca_existente = obtener_marca_por_nombre_repo(nombre)

    if marca_existente and marca_existente.id_marca != id_marca:
        raise ValueError("Ya existe otra marca con ese nombre.")

    try:
        resultado = actualizar_marca_repo(id_marca, nombre)

        if not resultado:
            raise ValueError("No se pudo actualizar la marca.")

        return True

    except IntegrityError:
        raise ValueError("No se pudo actualizar porque ese nombre ya está registrado.")


def eliminar_marca_negocio(id_marca, rol):
    validar_administrador(rol)
    validar_id(id_marca)

    marca = obtener_marca_por_id_repo(id_marca)

    if marca is None:
        raise ValueError(
            "No se encontró la marca que deseas desactivar."
        )

    resultado = eliminar_marca_repo(id_marca)

    if not resultado:
        raise ValueError("No se pudo desactivar la marca.")

    return True


def reactivar_marca_negocio(id_marca, rol):
    validar_administrador(rol)
    validar_id(id_marca)

    marca = obtener_marca_desactivada_por_id_repo(id_marca)

    if marca is None:
        raise ValueError("No se encontró una marca desactivada con ese ID.")

    resultado = reactivar_marca_repo(id_marca)

    if not resultado:
        raise ValueError("No se pudo reactivar la marca.")

    return True
