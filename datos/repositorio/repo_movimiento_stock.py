from datos.modelos.movimiento_stock import MovimientoStock


def listar_movimientos_repo():
    return list(MovimientoStock.select())


def listar_movimientos_por_producto_repo(id_producto):
    return list(
        MovimientoStock.select().where(
            MovimientoStock.id_producto == id_producto
        )
    )


def obtener_movimiento_por_id_repo(id_movimiento):
    return MovimientoStock.get_or_none(
        MovimientoStock.id_movimiento == id_movimiento
    )


def crear_movimiento_repo(id_producto, cantidad, tipo):
    objeto = MovimientoStock(
        id_producto=id_producto,
        cantidad=cantidad,
        tipo=tipo
    )
    objeto.save()
    return objeto
