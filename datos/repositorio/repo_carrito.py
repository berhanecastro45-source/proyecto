
from datos.modelos.carrito import Carrito


def obtener_carrito_por_id_repo(id_carrito):
    return Carrito.get_or_none(
        (Carrito.id_carrito == id_carrito) &
        (Carrito.activo == 1)
    )


def obtener_carrito_por_usuario_repo(id_usuario):
    return Carrito.get_or_none(
        (Carrito.id_usuario == id_usuario) &
        (Carrito.activo == 1)
    )


def listar_carritos_repo():
    return list(
        Carrito.select().where(Carrito.activo == 1)
    )


def crear_carrito_repo(id_usuario):
    objeto = Carrito(
        id_usuario=id_usuario,
        activo=1
    )
    objeto.save()
    return objeto


def eliminar_carrito_repo(id_carrito):
    carrito = obtener_carrito_por_id_repo(id_carrito)

    if carrito is None:
        return False

    carrito.activo = 0
    carrito.save()

    return True


def obtener_carrito_usuario_cualquier_estado_repo(id_usuario):
    return Carrito.get_or_none(Carrito.id_usuario == id_usuario)
