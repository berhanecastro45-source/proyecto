from datos.modelos.pago import Pago


def listar_pagos_repo():
    return list(Pago.select())


def obtener_pago_por_id_repo(id_pago):
    return Pago.get_or_none(Pago.id_pago == id_pago)


def listar_pagos_por_pedido_repo(id_pedido):
    return list(Pago.select().where(Pago.id_pedido == id_pedido))


def crear_pago_repo(id_pedido, id_forma_pago, monto, estado):
    objeto = Pago(
        id_pedido=id_pedido,
        id_forma_pago=id_forma_pago,
        monto=monto,
        estado=estado
    )
    objeto.save()
    return objeto


def actualizar_estado_pago_repo(id_pago, nuevo_estado):
    pago = obtener_pago_por_id_repo(id_pago)

    if pago is None:
        return False

    pago.estado = nuevo_estado
    return pago.save() > 0