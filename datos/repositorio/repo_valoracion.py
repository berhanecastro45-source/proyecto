from datos.modelos.valoracion import Valoracion


def listado_valoracion():
    return list(
        Valoracion.select().where(Valoracion.activo == 1)
    )


def listar_valoraciones_desactivadas_repo():
    return list(
        Valoracion.select().where(Valoracion.activo == 0)
    )


def listar_valoraciones_por_producto_repo(id_producto):
    return list(
        Valoracion.select().where(
            (Valoracion.id_producto == id_producto) &
            (Valoracion.activo == 1)
        )
    )


def listar_valoraciones_por_usuario_repo(id_usuario):
    return list(
        Valoracion.select().where(
            (Valoracion.id_usuario == id_usuario) &
            (Valoracion.activo == 1)
        )
    )


def obtener_valoracion_por_id_repo(id_valoracion):
    return Valoracion.get_or_none(
        (Valoracion.id_valoracion == id_valoracion) &
        (Valoracion.activo == 1)
    )


def obtener_valoracion_desactivada_por_id_repo(id_valoracion):
    return Valoracion.get_or_none(
        (Valoracion.id_valoracion == id_valoracion) &
        (Valoracion.activo == 0)
    )


def obtener_valoracion_usuario_producto_repo(id_usuario, id_producto):
    return Valoracion.get_or_none(
        (Valoracion.id_usuario == id_usuario) &
        (Valoracion.id_producto == id_producto) &
        (Valoracion.activo == 1)
    )


def obtener_valoracion_usuario_producto_inactiva_repo(
    id_usuario, id_producto
):
    return Valoracion.get_or_none(
        (Valoracion.id_usuario == id_usuario) &
        (Valoracion.id_producto == id_producto) &
        (Valoracion.activo == 0)
    )


def crear_valoracion_repo(
    id_usuario, id_producto, puntuacion, comentario=None
):
    objeto = Valoracion(
        id_usuario=id_usuario,
        id_producto=id_producto,
        puntuacion=puntuacion,
        comentario=comentario,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_valoracion_repo(
    id_valoracion, puntuacion, comentario=None
):
    valoracion = obtener_valoracion_por_id_repo(id_valoracion)

    if valoracion is None:
        return False

    valoracion.puntuacion = puntuacion
    valoracion.comentario = comentario

    return valoracion.save() > 0


def eliminar_valoracion_repo(id_valoracion):
    valoracion = obtener_valoracion_por_id_repo(id_valoracion)

    if valoracion is None:
        return False

    valoracion.activo = 0
    return valoracion.save() > 0


def reactivar_valoracion_repo(id_valoracion):
    valoracion = obtener_valoracion_desactivada_por_id_repo(
        id_valoracion
    )

    if valoracion is None:
        return False

    valoracion.activo = 1
    return valoracion.save() > 0

