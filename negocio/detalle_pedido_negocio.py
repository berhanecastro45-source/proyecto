from datos.repositorio.repo_detalle_pedido import (
    listar_detalles_por_pedido_repo,
    obtener_detalle_pedido_por_id_repo
)

from datos.repositorio.repo_pedido import (
    obtener_pedido_por_id_repo
)

from negocio.carrito_negocio import validar_usuario_sesion


def listar_detalles_pedido_negocio(usuario_actual, id_pedido):

    usuario = validar_usuario_sesion(usuario_actual)

    pedido = obtener_pedido_por_id_repo(id_pedido)

    if pedido is None:
        raise ValueError("El pedido no existe.")

    if pedido.id_usuario != usuario.id_usuario:
        if usuario.rol != "ADMINISTRADOR":
            raise PermissionError("No tienes permiso para consultar este pedido.")

    return listar_detalles_por_pedido_repo(id_pedido)


def obtener_detalle_pedido_negocio(usuario_actual, id_detalle):

    usuario = validar_usuario_sesion(usuario_actual)

    detalle = obtener_detalle_pedido_por_id_repo(id_detalle)

    if detalle is None:
        raise ValueError("El detalle del pedido no existe.")

    pedido = obtener_pedido_por_id_repo(detalle.id_pedido)

    if pedido is None:
        raise ValueError("El pedido asociado no existe.")

    if pedido.id_usuario != usuario.id_usuario:
        if usuario.rol != "ADMINISTRADOR":
            raise PermissionError("No tienes permiso para consultar este detalle.")

    return detalle
