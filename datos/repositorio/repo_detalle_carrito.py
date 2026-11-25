from datos.modelos.detalle_carrito import DetalleCarrito


def listar_detalles_por_carrito_repo(id_carrito):
    return list(
        DetalleCarrito.select().where(
            DetalleCarrito.id_carrito == id_carrito
        )
    )


def obtener_detalle_por_id_repo(id_detalle_carrito):
    return DetalleCarrito.get_or_none(
        DetalleCarrito.id_detalle_carrito == id_detalle_carrito
    )


def obtener_detalle_por_producto_repo(id_carrito, id_producto):
    return DetalleCarrito.get_or_none(
        (DetalleCarrito.id_carrito == id_carrito) &
        (DetalleCarrito.id_producto == id_producto)
    )


def crear_detalle_carrito_repo(
    id_carrito,
    id_producto,
    cantidad,
    precio_unitario,
    subtotal
):
    objeto = DetalleCarrito(
        id_carrito=id_carrito,
        id_producto=id_producto,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal
    )
    objeto.save()
    return objeto


def actualizar_detalle_carrito_repo(
    id_detalle_carrito,
    cantidad,
    subtotal
):
    detalle = obtener_detalle_por_id_repo(id_detalle_carrito)

    if detalle is None:
        return False

    detalle.cantidad = cantidad
    detalle.subtotal = subtotal
    detalle.save()

    return True


def eliminar_detalle_carrito_repo(id_detalle_carrito):
    detalle = obtener_detalle_por_id_repo(id_detalle_carrito)

    if detalle is None:
        return False

    detalle.delete_instance()

    return True
