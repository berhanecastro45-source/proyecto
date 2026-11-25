from negocio.producto_negocio import validar_producto
from decimal import Decimal
from peewee import IntegrityError

from datos.repositorio.repo_detalle_carrito import (
    listar_detalles_por_carrito_repo,
    obtener_detalle_por_id_repo,
    obtener_detalle_por_producto_repo,
    crear_detalle_carrito_repo,
    actualizar_detalle_carrito_repo,
    eliminar_detalle_carrito_repo
)

from datos.repositorio.repo_producto import obtener_producto_por_id_repo

from negocio.carrito_negocio import (
    validar_usuario_sesion,
    obtener_carrito_propio_negocio
)


def validar_id(id_registro, nombre="ID"):
    if isinstance(id_registro, bool) or not isinstance(id_registro, int) or id_registro <= 0:
        raise ValueError(f"El {nombre} debe ser un número entero positivo.")


def validar_cantidad(cantidad):
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un número entero positivo.")


def validar_detalle_propio(id_detalle_carrito, usuario_actual):
    validar_id(id_detalle_carrito, "ID de detalle")

    carrito = obtener_carrito_propio_negocio(usuario_actual)

    detalle = obtener_detalle_por_id_repo(id_detalle_carrito)

    if detalle is None or detalle.id_carrito != carrito.id_carrito:
        raise ValueError("El detalle no existe en tu carrito.")

    return detalle


def listar_detalles_carrito_negocio(usuario_actual):
    carrito = obtener_carrito_propio_negocio(usuario_actual)

    return listar_detalles_por_carrito_repo(carrito.id_carrito)


def buscar_detalle_carrito_negocio(id_detalle_carrito, usuario_actual):
    return validar_detalle_propio(id_detalle_carrito, usuario_actual)


def agregar_producto_carrito_negocio(id_producto, cantidad, usuario_actual):
    validar_usuario_sesion(usuario_actual)
    validar_cantidad(cantidad)

    carrito = obtener_carrito_propio_negocio(usuario_actual)
    producto = validar_producto(id_producto)

    detalle_existente = obtener_detalle_por_producto_repo(
        carrito.id_carrito,
        id_producto
    )

    cantidad_actual = detalle_existente.cantidad if detalle_existente else 0
    nueva_cantidad = cantidad_actual + cantidad

    if nueva_cantidad > producto.stock:
        raise ValueError("No hay suficiente stock disponible.")

    precio_unitario = Decimal(str(producto.precio))
    subtotal = precio_unitario * nueva_cantidad

    try:
        if detalle_existente:
            actualizar_detalle_carrito_repo(
                detalle_existente.id_detalle_carrito,
                nueva_cantidad,
                subtotal
            )

            return obtener_detalle_por_id_repo(
                detalle_existente.id_detalle_carrito
            )

        return crear_detalle_carrito_repo(
            carrito.id_carrito,
            id_producto,
            cantidad,
            precio_unitario,
            subtotal
        )

    except IntegrityError:
        raise ValueError("No se pudo agregar el producto al carrito.")


def actualizar_cantidad_detalle_negocio(
    id_detalle_carrito,
    cantidad,
    usuario_actual
):
    validar_cantidad(cantidad)

    detalle = validar_detalle_propio(id_detalle_carrito, usuario_actual)
    producto = validar_producto(detalle.id_producto)

    if cantidad > producto.stock:
        raise ValueError("No hay suficiente stock disponible.")

    subtotal = Decimal(str(detalle.precio_unitario)) * cantidad

    resultado = actualizar_detalle_carrito_repo(
        id_detalle_carrito,
        cantidad,
        subtotal
    )

    if not resultado:
        raise ValueError("No se pudo actualizar el detalle del carrito.")

    return obtener_detalle_por_id_repo(id_detalle_carrito)


def eliminar_producto_carrito_negocio(id_detalle_carrito, usuario_actual):
    validar_detalle_propio(id_detalle_carrito, usuario_actual)

    resultado = eliminar_detalle_carrito_repo(id_detalle_carrito)

    if not resultado:
        raise ValueError("No se pudo eliminar el producto del carrito.")

    return True
