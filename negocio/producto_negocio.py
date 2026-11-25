from auxiliares.validaciones import validar_administrador
from decimal import Decimal, InvalidOperation
from peewee import IntegrityError

from datos.repositorio.repo_producto import (
    listar_productos_repo,
    listar_productos_desactivados_repo,
    obtener_producto_por_id_repo,
    obtener_producto_desactivado_por_id_repo,
    crear_producto_repo,
    actualizar_producto_repo,
    eliminar_producto_repo,
    reactivar_producto_repo
)

from datos.repositorio.repo_categoria import obtener_categoria_por_id_repo
from datos.repositorio.repo_marca import obtener_marca_por_id_repo
from datos.repositorio.repo_proveedor import obtener_proveedor_por_id_repo


def validar_id(id_registro, nombre="ID"):
    if (
        isinstance(id_registro, bool)
        or not isinstance(id_registro, int)
        or id_registro <= 0
    ):
        raise ValueError(f"{nombre} debe ser un número entero positivo.")


def validar_nombre(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre del producto es obligatorio.")

    nombre = nombre.strip()

    if len(nombre) > 100:
        raise ValueError("El nombre no puede superar los 100 caracteres.")

    return nombre


def validar_descripcion(descripcion):
    if not isinstance(descripcion, str) or not descripcion.strip():
        raise ValueError("La descripción del producto es obligatoria.")

    return descripcion.strip()


def validar_precio(precio):
    try:
        precio = Decimal(str(precio))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("El precio debe ser un número válido.")

    if not precio.is_finite() or precio < 0:
        raise ValueError("El precio debe ser un número válido y no negativo.")

    if precio > Decimal("99999999.99"):
        raise ValueError("El precio supera el máximo permitido.")

    return precio


def validar_stock(stock, nombre="Stock"):
    if (
        isinstance(stock, bool)
        or not isinstance(stock, int)
        or stock < 0
    ):
        raise ValueError(f"{nombre} debe ser un número entero no negativo.")

    if stock > 2147483647:
        raise ValueError(f"{nombre} supera el máximo permitido.")

    return stock


def validar_categoria(id_categoria):
    validar_id(id_categoria, "El ID de la categoría")

    categoria = obtener_categoria_por_id_repo(id_categoria)

    if categoria is None:
        raise ValueError("No se encontró una categoría activa con ese ID.")

    return categoria


def validar_marca(id_marca):
    validar_id(id_marca, "El ID de la marca")

    marca = obtener_marca_por_id_repo(id_marca)

    if marca is None:
        raise ValueError("No se encontró una marca activa con ese ID.")

    return marca


def validar_proveedor(id_proveedor):
    validar_id(id_proveedor, "El ID del proveedor")

    proveedor = obtener_proveedor_por_id_repo(id_proveedor)

    if proveedor is None:
        raise ValueError("No se encontró un proveedor activo con ese ID.")

    return proveedor


def validar_producto(id_producto):
    validar_id(id_producto, "ID del producto")

    producto = obtener_producto_por_id_repo(id_producto)

    if producto is None:
        raise ValueError("El producto no existe o se encuentra desactivado.")

    return producto


def listar_productos_negocio():
    return listar_productos_repo()


def listar_productos_desactivados_negocio(rol):
    validar_administrador(rol)

    return listar_productos_desactivados_repo()


def buscar_producto_negocio(id_producto):
    validar_id(id_producto, "El ID del producto")

    producto = obtener_producto_por_id_repo(id_producto)

    if producto is None:
        raise ValueError("No se encontró el producto solicitado.")

    return producto


def buscar_producto_desactivado_negocio(id_producto, rol):
    validar_administrador(rol)
    validar_id(id_producto, "El ID del producto")

    producto = obtener_producto_desactivado_por_id_repo(id_producto)

    if producto is None:
        raise ValueError("No se encontró el producto desactivado solicitado.")

    return producto


def crear_producto_negocio(
    nombre,
    descripcion,
    precio,
    stock,
    stock_minimo,
    id_categoria,
    id_marca,
    id_proveedor,
    rol
):
    validar_administrador(rol)

    nombre = validar_nombre(nombre)
    descripcion = validar_descripcion(descripcion)
    precio = validar_precio(precio)
    stock = validar_stock(stock)
    stock_minimo = validar_stock(stock_minimo, "El stock mínimo")

    validar_categoria(id_categoria)
    validar_marca(id_marca)
    validar_proveedor(id_proveedor)

    try:
        return crear_producto_repo(
            nombre,
            descripcion,
            precio,
            stock,
            stock_minimo,
            id_categoria,
            id_marca,
            id_proveedor
        )

    except IntegrityError:
        raise ValueError(
            "No se pudo registrar el producto. Verifica que la categoría, marca y proveedor existan."
        )


def actualizar_producto_negocio(
    id_producto,
    nombre,
    descripcion,
    precio,
    stock_minimo,
    id_categoria,
    id_marca,
    id_proveedor,
    rol
):
    validar_administrador(rol)
    validar_id(id_producto, "El ID del producto")

    nombre = validar_nombre(nombre)
    descripcion = validar_descripcion(descripcion)
    precio = validar_precio(precio)
    stock_minimo = validar_stock(stock_minimo, "El stock mínimo")

    validar_categoria(id_categoria)
    validar_marca(id_marca)
    validar_proveedor(id_proveedor)

    producto = obtener_producto_por_id_repo(id_producto)

    if producto is None:
        raise ValueError("No se encontró el producto que deseas modificar.")

    try:
        resultado = actualizar_producto_repo(
            id_producto,
            nombre,
            descripcion,
            precio,
            stock_minimo,
            id_categoria,
            id_marca,
            id_proveedor
        )

        if not resultado:
            raise ValueError("No se pudo actualizar el producto.")

        return True

    except IntegrityError:
        raise ValueError(
            "No se pudo actualizar el producto. Verifica sus relaciones."
        )


def eliminar_producto_negocio(id_producto, rol):
    validar_administrador(rol)
    validar_id(id_producto, "El ID del producto")

    producto = obtener_producto_por_id_repo(id_producto)

    if producto is None:
        raise ValueError("No se encontró el producto que deseas desactivar.")

    resultado = eliminar_producto_repo(id_producto)

    if not resultado:
        raise ValueError("No se pudo desactivar el producto.")

    return True


def reactivar_producto_negocio(id_producto, rol):
    validar_administrador(rol)
    validar_id(id_producto, "El ID del producto")

    producto = obtener_producto_desactivado_por_id_repo(id_producto)

    if producto is None:
        raise ValueError("No se encontró el producto que deseas reactivar.")

    resultado = reactivar_producto_repo(id_producto)

    if not resultado:
        raise ValueError("No se pudo reactivar el producto.")

    return True

