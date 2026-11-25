
from datos.modelos.imagen_producto import ImagenProducto


def listar_imagenes_repo():
    return list(
        ImagenProducto.select().where(ImagenProducto.activo == 1)
    )


def listar_imagenes_por_producto_repo(id_producto):
    return list(
        ImagenProducto.select().where(
            (ImagenProducto.id_producto == id_producto) &
            (ImagenProducto.activo == 1)
        )
    )


def obtener_imagen_por_id_repo(id_imagen):
    return ImagenProducto.get_or_none(
        (ImagenProducto.id_imagen == id_imagen) &
        (ImagenProducto.activo == 1)
    )


def crear_imagen_repo(id_producto, url_imagen):
    objeto = ImagenProducto(
        id_producto=id_producto,
        url_imagen=url_imagen,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_imagen_repo(id_imagen, id_producto, url_imagen):
    imagen = obtener_imagen_por_id_repo(id_imagen)

    if imagen is None:
        return False

    imagen.id_producto = id_producto
    imagen.url_imagen = url_imagen
    imagen.save()

    return True


def eliminar_imagen_repo(id_imagen):
    imagen = obtener_imagen_por_id_repo(id_imagen)

    if imagen is None:
        return False

    imagen.activo = 0
    imagen.save()

    return True
