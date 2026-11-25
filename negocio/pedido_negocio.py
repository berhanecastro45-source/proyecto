
from datetime import date
from decimal import Decimal

from datos.conexion import DB
from datos.repositorio.repo_pedido import (
    listar_pedidos_repo,
    listar_pedidos_por_usuario_repo,
    obtener_pedido_por_id_repo,
    actualizar_estado_pedido_repo,
    crear_pedido_repo
)

from datos.repositorio.repo_detalle_pedido import (
    crear_detalle_pedido_repo,
    listar_detalles_por_pedido_repo
)
from datos.repositorio.repo_pago import (
    crear_pago_repo,
    listar_pagos_por_pedido_repo,
    actualizar_estado_pago_repo
)
from datos.repositorio.repo_movimiento_stock import crear_movimiento_repo
from datos.repositorio.repo_forma_pago import obtener_forma_pago_por_id_repo

from datos.repositorio.repo_detalle_carrito import (
    listar_detalles_por_carrito_repo,
    eliminar_detalle_carrito_repo
)

from datos.repositorio.repo_producto import (
    obtener_producto_por_id_repo,
    obtener_producto_para_actualizar_repo,
    actualizar_stock_producto_repo
)

from datos.repositorio.repo_cupon import obtener_cupon_por_codigo_repo

from auxiliares.validaciones import es_administrador
from negocio.carrito_negocio import (
    validar_usuario_sesion,
    obtener_carrito_propio_negocio
)


def obtener_historial_pedidos_negocio(usuario_actual):

    usuario = validar_usuario_sesion(usuario_actual)

    return listar_pedidos_por_usuario_repo(usuario.id_usuario)


def listar_pedidos_disponibles_negocio(usuario_actual):

    usuario = validar_usuario_sesion(usuario_actual)

    if es_administrador(usuario):
        return listar_pedidos_repo()

    return listar_pedidos_por_usuario_repo(usuario.id_usuario)


def procesar_checkout_negocio(usuario_actual, direccion_envio, id_forma_pago, codigo_cupon=None):

    usuario = validar_usuario_sesion(usuario_actual)

    if not direccion_envio or not direccion_envio.strip() or len(direccion_envio.strip()) > 300:
        raise ValueError("Debe ingresar una dirección de envío válida.")

    forma_pago = obtener_forma_pago_por_id_repo(id_forma_pago)

    if forma_pago is None or forma_pago.activo != 1:
        raise ValueError("La forma de pago no está disponible.")

    carrito = obtener_carrito_propio_negocio(usuario)
    detalles = listar_detalles_por_carrito_repo(carrito.id_carrito)

    if not detalles:
        raise ValueError("El carrito está vacío.")

    total = Decimal("0.00")

    for detalle in detalles:

        producto = obtener_producto_por_id_repo(detalle.id_producto)

        if producto is None or producto.stock < detalle.cantidad:
            raise ValueError("No hay suficiente stock de uno de los productos.")

        total += Decimal(str(detalle.precio_unitario)) * detalle.cantidad

    cupon = None

    if codigo_cupon is not None:

        cupon = obtener_cupon_por_codigo_repo(codigo_cupon.strip().upper())

        if cupon is None or cupon.activo != 1 or date.today() < cupon.fecha_inicio or date.today() > cupon.fecha_fin:
            raise ValueError("El cupón no es válido.")

        total -= total * Decimal(str(cupon.descuento)) / Decimal("100")

    total = max(total, Decimal("0.00")).quantize(Decimal("0.01"))

    with DB.atomic():

        pedido = crear_pedido_repo(
            usuario.id_usuario,
            cupon.id_cupon if cupon else None,
            direccion_envio.strip(),
            "PENDIENTE",
            total
        )

        for detalle in detalles:

            producto = obtener_producto_para_actualizar_repo(detalle.id_producto)

            if producto is None or producto.stock < detalle.cantidad:
                raise ValueError("No hay suficiente stock de uno de los productos.")

            precio = Decimal(str(detalle.precio_unitario))
            subtotal = precio * detalle.cantidad

            crear_detalle_pedido_repo(
                pedido.id_pedido,
                producto.id_producto,
                detalle.cantidad,
                precio,
                subtotal
            )

            resultado = actualizar_stock_producto_repo(
                producto.id_producto,
                producto.stock - detalle.cantidad
            )

            if not resultado:
                raise ValueError("No se pudo actualizar el stock de un producto.")

            crear_movimiento_repo(
                producto.id_producto,
                detalle.cantidad,
                "SALIDA"
            )

            eliminar_detalle_carrito_repo(detalle.id_detalle_carrito)

        if total > 0:

            crear_pago_repo(
                pedido.id_pedido,
                id_forma_pago,
                total,
                "PENDIENTE"
            )

    return pedido.id_pedido


def cancelar_pedido_negocio(usuario_actual, id_pedido):
    """Cancela un pedido PENDIENTE: devuelve el stock y rechaza sus pagos."""
    usuario = validar_usuario_sesion(usuario_actual)

    if isinstance(id_pedido, bool) or not isinstance(id_pedido, int) or id_pedido <= 0:
        raise ValueError("El ID del pedido debe ser un número entero positivo.")

    pedido = obtener_pedido_por_id_repo(id_pedido)

    if pedido is None:
        raise ValueError("El pedido no existe.")

    if not es_administrador(usuario) and pedido.id_usuario != usuario.id_usuario:
        raise PermissionError("Solo puedes cancelar tus propios pedidos.")

    if pedido.estado != "PENDIENTE":
        raise ValueError("Solo se pueden cancelar pedidos en estado PENDIENTE.")

    pagos = listar_pagos_por_pedido_repo(id_pedido)

    if any(pago.estado == "APROBADO" for pago in pagos):
        raise ValueError("El pedido tiene un pago aprobado y no puede cancelarse.")

    with DB.atomic():
        for detalle in listar_detalles_por_pedido_repo(id_pedido):
            producto = obtener_producto_para_actualizar_repo(detalle.id_producto)

            if producto is not None:
                actualizar_stock_producto_repo(
                    producto.id_producto,
                    producto.stock + detalle.cantidad
                )
                crear_movimiento_repo(
                    producto.id_producto,
                    detalle.cantidad,
                    "ENTRADA"
                )

        for pago in pagos:
            actualizar_estado_pago_repo(pago.id_pago, "RECHAZADO")

        actualizar_estado_pedido_repo(id_pedido, "CANCELADO")
