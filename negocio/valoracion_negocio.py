from peewee import IntegrityError
from datos.repositorio.repo_producto import obtener_producto_por_id_repo
from datos.repositorio.repo_valoracion import (
    listado_valoracion,
    listar_valoraciones_desactivadas_repo,
    listar_valoraciones_por_producto_repo,
    listar_valoraciones_por_usuario_repo,
    obtener_valoracion_por_id_repo,
    obtener_valoracion_desactivada_por_id_repo,
    obtener_valoracion_usuario_producto_repo,
    obtener_valoracion_usuario_producto_inactiva_repo,
    crear_valoracion_repo,
    actualizar_valoracion_repo,
    eliminar_valoracion_repo,
    reactivar_valoracion_repo
)

from negocio.carrito_negocio import (
    validar_usuario_sesion,
    validar_administrador
)


def validar_id(id_registro, nombre="ID"):
    if (
        isinstance(id_registro, bool)
        or not isinstance(id_registro, int)
        or id_registro <= 0
    ):
        raise ValueError(
            f"El {nombre} debe ser un número entero positivo."
        )


def validar_puntuacion(puntuacion):
    if (
        isinstance(puntuacion, bool)
        or not isinstance(puntuacion, int)
        or puntuacion < 1
        or puntuacion > 5
    ):
        raise ValueError("La puntuación debe estar entre 1 y 5.")


def validar_comentario(comentario):
    if comentario is None or comentario == "":
        return None

    if not isinstance(comentario, str):
        raise ValueError("El comentario debe ser texto.")

    comentario = comentario.strip()

    if len(comentario) > 500:
        raise ValueError(
            "El comentario no puede superar los 500 caracteres."
        )

    return comentario or None


def validar_producto(id_producto):
    validar_id(id_producto, "ID del producto")

    producto = obtener_producto_por_id_repo(id_producto)

    if producto is None:
        raise ValueError("El producto no existe o está desactivado.")

    return producto


def validar_valoracion_propia(id_valoracion, usuario_actual):
    validar_id(id_valoracion, "ID de la valoración")

    usuario = validar_usuario_sesion(usuario_actual)

    valoracion = obtener_valoracion_por_id_repo(id_valoracion)

    if valoracion is None:
        raise ValueError("La valoración no existe.")

    if valoracion.id_usuario != usuario.id_usuario:
        raise PermissionError(
            "No puedes modificar esta valoración."
        )

    return valoracion


def validar_valoracion_inactiva_propia(
    id_valoracion, usuario_actual
):
    validar_id(id_valoracion, "ID de la valoración")

    usuario = validar_usuario_sesion(usuario_actual)

    valoracion = obtener_valoracion_desactivada_por_id_repo(
        id_valoracion
    )

    if valoracion is None:
        raise ValueError(
            "La valoración no existe o ya está activa."
        )

    if valoracion.id_usuario != usuario.id_usuario:
        raise PermissionError(
            "No puedes reactivar esta valoración."
        )

    return valoracion


def listar_valoraciones_negocio(usuario_actual):
    validar_administrador(usuario_actual)

    return listado_valoracion()


def listar_valoraciones_producto_negocio(id_producto):
    validar_producto(id_producto)

    return listar_valoraciones_por_producto_repo(id_producto)


def listar_valoraciones_usuario_negocio(usuario_actual):
    usuario = validar_usuario_sesion(usuario_actual)

    return listar_valoraciones_por_usuario_repo(
        usuario.id_usuario
    )


def listar_valoraciones_desactivadas_negocio(usuario_actual):
    usuario = validar_usuario_sesion(usuario_actual)

    valoraciones = listar_valoraciones_desactivadas_repo()

    if usuario.rol == "ADMINISTRADOR":
        return valoraciones

    valoraciones_usuario = []

    for valoracion in valoraciones:
        if valoracion.id_usuario == usuario.id_usuario:
            valoraciones_usuario.append(valoracion)

    return valoraciones_usuario


def buscar_valoracion_negocio(id_valoracion, usuario_actual):
    return validar_valoracion_propia(
        id_valoracion,
        usuario_actual
    )


def crear_valoracion_negocio(
    id_producto,
    puntuacion,
    comentario,
    usuario_actual
):
    usuario = validar_usuario_sesion(usuario_actual)

    validar_producto(id_producto)
    validar_puntuacion(puntuacion)
    comentario = validar_comentario(comentario)

    valoracion_existente = obtener_valoracion_usuario_producto_repo(
        usuario.id_usuario,
        id_producto
    )

    if valoracion_existente is not None:
        raise ValueError(
            "Ya has valorado este producto."
        )

    valoracion_inactiva = (
        obtener_valoracion_usuario_producto_inactiva_repo(
            usuario.id_usuario,
            id_producto
        )
    )

    if valoracion_inactiva is not None:
        raise ValueError(
            "Ya tienes una valoración desactivada para este producto. "
            "Debes reactivarla en lugar de crear otra."
        )

    try:
        return crear_valoracion_repo(
            usuario.id_usuario,
            id_producto,
            puntuacion,
            comentario
        )

    except IntegrityError:
        raise ValueError(
            "Ya existe una valoración para este producto."
        )


def actualizar_valoracion_negocio(
    id_valoracion,
    puntuacion,
    comentario,
    usuario_actual
):
    validar_valoracion_propia(id_valoracion, usuario_actual)

    validar_puntuacion(puntuacion)
    comentario = validar_comentario(comentario)

    resultado = actualizar_valoracion_repo(
        id_valoracion,
        puntuacion,
        comentario
    )

    if not resultado:
        raise ValueError(
            "No se pudo actualizar la valoración."
        )

    return True


def eliminar_valoracion_negocio(id_valoracion, usuario_actual):
    validar_valoracion_propia(id_valoracion, usuario_actual)

    resultado = eliminar_valoracion_repo(id_valoracion)

    if not resultado:
        raise ValueError(
            "No se pudo desactivar la valoración."
        )

    return True


def reactivar_valoracion_negocio(id_valoracion, usuario_actual):
    validar_valoracion_inactiva_propia(
        id_valoracion,
        usuario_actual
    )

    try:
        resultado = reactivar_valoracion_repo(id_valoracion)

        if not resultado:
            raise ValueError(
                "No se pudo reactivar la valoración."
            )

        return True

    except IntegrityError:
        raise ValueError(
            "No se pudo reactivar la valoración porque existe "
            "un registro que entra en conflicto con ella."
        )

