from peewee import IntegrityError

from datos.repositorio.repo_carrito import (
    obtener_carrito_por_id_repo,
    obtener_carrito_por_usuario_repo,
    listar_carritos_repo,
    crear_carrito_repo,
    eliminar_carrito_repo
)

from datos.repositorio.repo_usuario import obtener_usuario_activo_por_id_repo
from datos.repositorio.repo_carrito import obtener_carrito_usuario_cualquier_estado_repo


def validar_usuario_sesion(usuario_actual):
    if usuario_actual is None:
        raise PermissionError("Debes iniciar sesión.")

    id_usuario = getattr(usuario_actual, "id_usuario", None)

    if isinstance(id_usuario, bool) or not isinstance(id_usuario, int) or id_usuario <= 0:
        raise PermissionError("La sesión del usuario no es válida.")

    usuario = obtener_usuario_activo_por_id_repo(id_usuario)

    if usuario is None:
        raise PermissionError("El usuario no existe o está inactivo.")

    return usuario


def validar_administrador(usuario_actual):
    usuario = validar_usuario_sesion(usuario_actual)

    if usuario.rol.strip().upper() != "ADMINISTRADOR":
        raise PermissionError("No tienes permisos para realizar esta acción.")

    return usuario


def validar_id(id_registro, nombre="ID"):
    if isinstance(id_registro, bool) or not isinstance(id_registro, int) or id_registro <= 0:
        raise ValueError(f"El {nombre} debe ser un número entero positivo.")


def listar_carritos_negocio(usuario_actual):
    validar_administrador(usuario_actual)
    return listar_carritos_repo()


def buscar_carrito_negocio(id_carrito, usuario_actual):
    validar_administrador(usuario_actual)
    validar_id(id_carrito, "ID de carrito")

    carrito = obtener_carrito_por_id_repo(id_carrito)

    if carrito is None:
        raise ValueError("El carrito no existe o está inactivo.")

    return carrito


def buscar_carrito_por_usuario_negocio(id_usuario, usuario_actual):
    validar_administrador(usuario_actual)
    validar_id(id_usuario, "ID de usuario")

    usuario = obtener_usuario_activo_por_id_repo(id_usuario)

    if usuario is None:
        raise ValueError("El usuario no existe o está inactivo.")

    carrito = obtener_carrito_por_usuario_repo(id_usuario)

    if carrito is None:
        raise ValueError("El usuario no tiene un carrito activo.")

    return carrito


def obtener_carrito_propio_negocio(usuario_actual):
    usuario = validar_usuario_sesion(usuario_actual)

    carrito = obtener_carrito_usuario_cualquier_estado_repo(usuario.id_usuario)

    if carrito is not None:
        if carrito.activo == 0:
            carrito.activo = 1
            carrito.save()

        return carrito

    try:
        return crear_carrito_repo(usuario.id_usuario)

    except IntegrityError:
        carrito = obtener_carrito_usuario_cualquier_estado_repo(usuario.id_usuario)

        if carrito is None:
            raise ValueError("No se pudo obtener el carrito del usuario.")

        if carrito.activo == 0:
            carrito.activo = 1
            carrito.save()

        return carrito


def eliminar_carrito_negocio(id_carrito, usuario_actual):
    validar_administrador(usuario_actual)
    validar_id(id_carrito, "ID de carrito")

    carrito = obtener_carrito_por_id_repo(id_carrito)

    if carrito is None:
        raise ValueError("El carrito no existe o está inactivo.")

    resultado = eliminar_carrito_repo(id_carrito)

    if not resultado:
        raise ValueError("No se pudo desactivar el carrito.")

    return True
