from auxiliares.validaciones import validar_administrador
from peewee import IntegrityError

from datos.repositorio.repo_categoria import (
    listar_categorias_repo,
    listar_categorias_desactivadas_repo,
    obtener_categoria_por_id_repo,
    obtener_categoria_desactivada_por_id_repo,
    obtener_categoria_por_nombre_repo,
    crear_categoria_repo,
    actualizar_categoria_repo,
    eliminar_categoria_repo,
    reactivar_categoria_repo
)


def validar_id(id_categoria):
    if isinstance(id_categoria, bool) or not isinstance(id_categoria, int) or id_categoria <= 0:
        raise ValueError("El ID debe ser un número entero positivo.")


def validar_nombre(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre de la categoría es obligatorio.")

    nombre = nombre.strip()

    if nombre.isdigit():
        raise ValueError("El nombre no puede contener solamente números.")

    if len(nombre) > 100:
        raise ValueError("El nombre no puede superar los 100 caracteres.")

    return nombre


def validar_descripcion(descripcion):
    if not isinstance(descripcion, str) or not descripcion.strip():
        raise ValueError("La descripción de la categoría es obligatoria.")

    descripcion = descripcion.strip()

    if descripcion.isdigit():
        raise ValueError("La descripción no puede contener solamente números.")

    if len(descripcion) > 255:
        raise ValueError("La descripción no puede superar los 255 caracteres.")

    return descripcion


def listar_categorias_negocio():
    return listar_categorias_repo()


def listar_categorias_desactivadas_negocio(rol):
    validar_administrador(rol)
    return listar_categorias_desactivadas_repo()


def buscar_categoria_negocio(id_categoria):
    validar_id(id_categoria)

    categoria = obtener_categoria_por_id_repo(id_categoria)

    if categoria is None:
        raise ValueError("No se encontró la categoría solicitada.")

    return categoria


def crear_categoria_negocio(nombre, descripcion, rol):
    validar_administrador(rol)

    nombre = validar_nombre(nombre)
    descripcion = validar_descripcion(descripcion)

    categoria = obtener_categoria_por_nombre_repo(nombre)

    if categoria:
        if categoria.activo == 0:
            raise ValueError(
                "Esta categoría está desactivada. Puedes reactivarla desde el menú."
            )

        raise ValueError("Ya existe una categoría con ese nombre.")

    try:
        return crear_categoria_repo(nombre, descripcion)

    except IntegrityError:
        raise ValueError("Ese nombre ya está registrado.")


def actualizar_categoria_negocio(id_categoria, nombre, descripcion, rol):
    validar_administrador(rol)
    validar_id(id_categoria)

    nombre = validar_nombre(nombre)
    descripcion = validar_descripcion(descripcion)

    categoria = obtener_categoria_por_id_repo(id_categoria)

    if categoria is None:
        raise ValueError("No se encontró la categoría que deseas modificar.")

    categoria_existente = obtener_categoria_por_nombre_repo(nombre)

    if categoria_existente and categoria_existente.id_categoria != id_categoria:
        raise ValueError("Ya existe otra categoría con ese nombre.")

    try:
        resultado = actualizar_categoria_repo(
            id_categoria,
            nombre,
            descripcion
        )

        if not resultado:
            raise ValueError("No se pudo actualizar la categoría.")

        return True

    except IntegrityError:
        raise ValueError("Ese nombre ya está registrado.")


def eliminar_categoria_negocio(id_categoria, rol):
    validar_administrador(rol)
    validar_id(id_categoria)

    categoria = obtener_categoria_por_id_repo(id_categoria)

    if categoria is None:
        raise ValueError("No se encontró la categoría que deseas desactivar.")

    resultado = eliminar_categoria_repo(id_categoria)

    if not resultado:
        raise ValueError("No se pudo desactivar la categoría.")

    return True


def reactivar_categoria_negocio(id_categoria, rol):
    validar_administrador(rol)
    validar_id(id_categoria)

    categoria = obtener_categoria_desactivada_por_id_repo(id_categoria)

    if categoria is None:
        raise ValueError("No se encontró una categoría desactivada con ese ID.")

    resultado = reactivar_categoria_repo(id_categoria)

    if not resultado:
        raise ValueError("No se pudo reactivar la categoría.")

    return True