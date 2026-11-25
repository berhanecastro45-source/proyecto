from datos.modelos.detalle_pedido import DetallePedido


def listar_detalles_por_pedido_repo(id_pedido):
    return list(
        DetallePedido.select().where(
            DetallePedido.id_pedido == id_pedido
        )
    )


def obtener_detalle_pedido_por_id_repo(id_detalle):
    return DetallePedido.get_or_none(
        DetallePedido.id_detalle == id_detalle
    )


def crear_detalle_pedido_repo(
    id_pedido,
    id_producto,
    cantidad,
    precio_unitario,
    subtotal
):
    objeto = DetallePedido(
        id_pedido=id_pedido,
        id_producto=id_producto,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal
    )
    objeto.save()
    return objeto


def eliminar_detalles_por_pedido_repo(id_pedido):
    return DetallePedido.delete().where(
        DetallePedido.id_pedido == id_pedido
    ).execute()
