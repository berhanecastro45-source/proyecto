
from datos.modelos.pedido import Pedido


def listar_pedidos_repo():
    return list(Pedido.select())


def obtener_pedido_por_id_repo(id_pedido):
    return Pedido.get_or_none(
        Pedido.id_pedido == id_pedido
    )


def listar_pedidos_por_usuario_repo(id_usuario):
    return list(
        Pedido.select().where(
            Pedido.id_usuario == id_usuario
        )
    )


def crear_pedido_repo(
    id_usuario,
    id_cupon,
    direccion_envio,
    estado,
    total
):
    objeto = Pedido(
        id_usuario=id_usuario,
        id_cupon=id_cupon,
        direccion_envio=direccion_envio,
        estado=estado,
        total=total
    )
    objeto.save()
    return objeto


def actualizar_estado_pedido_repo(id_pedido, nuevo_estado):
    pedido = obtener_pedido_por_id_repo(id_pedido)

    if pedido is None:
        return False

    pedido.estado = nuevo_estado
    pedido.save()

    return True
