
from datos.modelos.producto import Producto
from datos.modelos.categoria import Categoria
from datos.modelos.marca import Marca
from datos.modelos.proveedor import Proveedor


def listar_productos_repo():
    return list(
        Producto
        .select(
            Producto,
            Categoria.nombre.alias("nombre_categoria"),
            Marca.nombre.alias("nombre_marca"),
            Proveedor.nombre.alias("nombre_proveedor")
        )
        .objects()
        .join(
            Categoria,
            on=(Producto.id_categoria == Categoria.id_categoria)
        )
        .switch(Producto)
        .join(
            Marca,
            on=(Producto.id_marca == Marca.id_marca)
        )
        .switch(Producto)
        .join(
            Proveedor,
            on=(Producto.id_proveedor == Proveedor.id_proveedor)
        )
        .where(Producto.activo == 1)
    )


def listar_productos_desactivados_repo():
    return list(
        Producto
        .select(
            Producto,
            Categoria.nombre.alias("nombre_categoria"),
            Marca.nombre.alias("nombre_marca"),
            Proveedor.nombre.alias("nombre_proveedor")
        )
        .objects()
        .join(
            Categoria,
            on=(Producto.id_categoria == Categoria.id_categoria)
        )
        .switch(Producto)
        .join(
            Marca,
            on=(Producto.id_marca == Marca.id_marca)
        )
        .switch(Producto)
        .join(
            Proveedor,
            on=(Producto.id_proveedor == Proveedor.id_proveedor)
        )
        .where(Producto.activo == 0)
    )


def obtener_producto_por_id_repo(id_producto):
    return (
        Producto
        .select(
            Producto,
            Categoria.nombre.alias("nombre_categoria"),
            Marca.nombre.alias("nombre_marca"),
            Proveedor.nombre.alias("nombre_proveedor")
        )
        .objects()
        .join(
            Categoria,
            on=(Producto.id_categoria == Categoria.id_categoria)
        )
        .switch(Producto)
        .join(
            Marca,
            on=(Producto.id_marca == Marca.id_marca)
        )
        .switch(Producto)
        .join(
            Proveedor,
            on=(Producto.id_proveedor == Proveedor.id_proveedor)
        )
        .where(
            (Producto.id_producto == id_producto) &
            (Producto.activo == 1)
        )
        .get_or_none()
    )


def obtener_producto_desactivado_por_id_repo(id_producto):
    return Producto.get_or_none(
        (Producto.id_producto == id_producto) &
        (Producto.activo == 0)
    )


def obtener_producto_por_nombre_repo(nombre):
    return Producto.get_or_none(
        Producto.nombre == nombre
    )


def crear_producto_repo(
    nombre,
    descripcion,
    precio,
    stock,
    stock_minimo,
    id_categoria,
    id_marca,
    id_proveedor
):
    objeto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
        stock_minimo=stock_minimo,
        id_categoria=id_categoria,
        id_marca=id_marca,
        id_proveedor=id_proveedor,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_producto_repo(
    id_producto,
    nombre,
    descripcion,
    precio,
    stock_minimo,
    id_categoria,
    id_marca,
    id_proveedor
):
    producto = obtener_producto_por_id_repo(id_producto)

    if producto is None:
        return False

    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.precio = precio
    producto.stock_minimo = stock_minimo
    producto.id_categoria = id_categoria
    producto.id_marca = id_marca
    producto.id_proveedor = id_proveedor

    producto.save()

    return True


def actualizar_stock_producto_repo(id_producto, nuevo_stock):
    producto = obtener_producto_por_id_repo(id_producto)

    if producto is None:
        return False

    producto.stock = nuevo_stock
    producto.save()

    return True


def eliminar_producto_repo(id_producto):
    producto = obtener_producto_por_id_repo(id_producto)

    if producto is None:
        return False

    producto.activo = 0
    producto.save()

    return True


def reactivar_producto_repo(id_producto):
    producto = obtener_producto_desactivado_por_id_repo(id_producto)

    if producto is None:
        return False

    producto.activo = 1
    producto.save()

    return True


def obtener_producto_para_actualizar_repo(id_producto):
    """Producto activo con bloqueo de fila (usar dentro de una transacción)."""
    return (
        Producto.select()
        .where((Producto.id_producto == id_producto) & (Producto.activo == 1))
        .for_update()
        .get_or_none()
    )


