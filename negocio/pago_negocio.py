from datos.repositorio.repo_pago import (
    listar_pagos_repo,
    obtener_pago_por_id_repo,
    listar_pagos_por_pedido_repo,
    actualizar_estado_pago_repo
)

from datos.repositorio.repo_pedido import obtener_pedido_por_id_repo
from negocio.carrito_negocio import validar_usuario_sesion


def validar_id(id):
    if isinstance(id, bool) or not isinstance(id, int) or id <= 0:
        raise ValueError("El ID ingresado no es válido.")


def listar_pagos_negocio(usuario_actual):
    usuario = validar_usuario_sesion(usuario_actual)

    if usuario.rol != "ADMINISTRADOR":
        raise PermissionError(
            "No tienes permiso para consultar todos los pagos."
        )

    return listar_pagos_repo()


def obtener_pago_negocio(usuario_actual, id_pago):
    usuario = validar_usuario_sesion(usuario_actual)
    validar_id(id_pago)

    pago = obtener_pago_por_id_repo(id_pago)

    if pago is None:
        raise ValueError("El pago no existe.")

    pedido = obtener_pedido_por_id_repo(pago.id_pedido)

    if pedido is None:
        raise ValueError("El pedido asociado no existe.")

    if pedido.id_usuario != usuario.id_usuario:
        if usuario.rol != "ADMINISTRADOR":
            raise PermissionError(
                "No tienes permiso para consultar este pago."
            )

    return pago


def listar_pagos_por_pedido_negocio(usuario_actual, id_pedido):
    usuario = validar_usuario_sesion(usuario_actual)
    validar_id(id_pedido)

    pedido = obtener_pedido_por_id_repo(id_pedido)

    if pedido is None:
        raise ValueError("El pedido no existe.")

    if pedido.id_usuario != usuario.id_usuario:
        if usuario.rol != "ADMINISTRADOR":
            raise PermissionError(
                "No tienes permiso para consultar los pagos de este pedido."
            )

    return listar_pagos_por_pedido_repo(id_pedido)


def actualizar_estado_pago_negocio(usuario_actual, id_pago, nuevo_estado):
    usuario = validar_usuario_sesion(usuario_actual)

    if usuario.rol != "ADMINISTRADOR":
        raise PermissionError(
            "No tienes permiso para modificar el estado de los pagos."
        )

    validar_id(id_pago)
    obtener_pago_negocio(usuario_actual, id_pago)

    estados_validos = ["PENDIENTE", "APROBADO", "RECHAZADO"]

    if nuevo_estado not in estados_validos:
        raise ValueError("El estado del pago no es válido.")

    resultado = actualizar_estado_pago_repo(id_pago, nuevo_estado)

    if not resultado:
        raise ValueError("No se pudo actualizar el estado del pago.")

    return True


