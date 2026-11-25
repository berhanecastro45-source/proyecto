from negocio.producto_negocio import validar_producto
from auxiliares.validaciones import validar_administrador
from peewee import IntegrityError

from datos.repositorio.repo_movimiento_stock import (
    listar_movimientos_repo,
    listar_movimientos_por_producto_repo,
    obtener_movimiento_por_id_repo,
    crear_movimiento_repo
)

from datos.repositorio.repo_producto import (
    obtener_producto_por_id_repo,
    actualizar_stock_producto_repo
)

from datos.conexion import DB


def validar_id(id_registro, nombre="ID"):
    if (
        isinstance(id_registro, bool)
        or not isinstance(id_registro, int)
        or id_registro <= 0
    ):
        raise ValueError(f"El {nombre} debe ser un número entero positivo.")


def validar_cantidad(cantidad):
    if (
        isinstance(cantidad, bool)
        or not isinstance(cantidad, int)
        or cantidad <= 0
    ):
        raise ValueError("La cantidad debe ser un número entero mayor que cero.")


def validar_tipo(tipo):
    if not isinstance(tipo, str):
        raise ValueError("El tipo de movimiento debe ser un texto.")

    tipo = tipo.strip().upper()

    if tipo not in ("ENTRADA", "SALIDA"):
        raise ValueError("El tipo de movimiento debe ser ENTRADA o SALIDA.")

    return tipo


def listar_movimientos_negocio():
    return listar_movimientos_repo()


def listar_movimientos_por_producto_negocio(id_producto):
    validar_producto(id_producto)
    return listar_movimientos_por_producto_repo(id_producto)


def buscar_movimiento_negocio(id_movimiento):
    validar_id(id_movimiento, "ID del movimiento")

    movimiento = obtener_movimiento_por_id_repo(id_movimiento)

    if movimiento is None:
        raise ValueError("El movimiento no existe.")

    return movimiento


def registrar_movimiento_negocio(id_producto, cantidad, tipo, rol):
    validar_administrador(rol)

    producto = validar_producto(id_producto)
    validar_cantidad(cantidad)
    tipo = validar_tipo(tipo)

    if tipo == "SALIDA" and cantidad > producto.stock:
        raise ValueError(
            "No hay suficiente stock disponible para realizar esta salida."
        )

    nuevo_stock = producto.stock + cantidad if tipo == "ENTRADA" else producto.stock - cantidad

    if nuevo_stock > 2147483647:
        raise ValueError("La cantidad supera el límite permitido para el stock.")

    try:
        # Ambas operaciones deben confirmarse juntas: si una falla,
        # la transacción revierte los cambios para mantener el inventario
        # y su historial sincronizados.
        with DB.atomic():
            movimiento = crear_movimiento_repo(
                id_producto,
                cantidad,
                tipo
            )

            resultado = actualizar_stock_producto_repo(
                id_producto,
                nuevo_stock
            )

            if not resultado:
                raise ValueError("No se pudo actualizar el stock del producto.")

        return movimiento

    except IntegrityError:
        raise ValueError(
            "No se pudo registrar el movimiento. Verifica que el producto exista."
        )

