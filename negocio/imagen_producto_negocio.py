from negocio.producto_negocio import validar_producto
from auxiliares.validaciones import validar_administrador
from peewee import IntegrityError

from datos.repositorio.repo_imagen_producto import (
    listar_imagenes_repo,
    listar_imagenes_por_producto_repo,
    obtener_imagen_por_id_repo,
    crear_imagen_repo,
    actualizar_imagen_repo,
    eliminar_imagen_repo
)

from datos.repositorio.repo_producto import (
    obtener_producto_por_id_repo
)


def validar_id(id_registro, nombre="ID"):
    if isinstance(id_registro, bool) or not isinstance(id_registro, int) or id_registro <= 0:
        raise ValueError(f"El {nombre} debe ser un número entero positivo.")


def validar_url_imagen(url_imagen):
    if not isinstance(url_imagen, str):
        raise ValueError("La URL de la imagen debe ser un texto.")

    url_imagen = url_imagen.strip()

    if not url_imagen:
        raise ValueError("La URL de la imagen es obligatoria.")

    if len(url_imagen) > 255:
        raise ValueError("La URL de la imagen no puede superar los 255 caracteres.")

    return url_imagen


def listar_imagenes_negocio():
    return listar_imagenes_repo()


def listar_imagenes_por_producto_negocio(id_producto):
    validar_id(id_producto, "ID del producto")
    validar_producto(id_producto)

    return listar_imagenes_por_producto_repo(id_producto)


def buscar_imagen_negocio(id_imagen):
    validar_id(id_imagen, "ID de la imagen")

    imagen = obtener_imagen_por_id_repo(id_imagen)

    if imagen is None:
        raise ValueError("La imagen no existe o se encuentra desactivada.")

    return imagen


def crear_imagen_negocio(id_producto, url_imagen, rol):
    validar_administrador(rol)
    validar_producto(id_producto)

    url_imagen = validar_url_imagen(url_imagen)

    try:
        return crear_imagen_repo(id_producto, url_imagen)

    except IntegrityError:
        raise ValueError(
            "No se pudo registrar la imagen. Verifica los datos del producto."
        )


def actualizar_imagen_negocio(id_imagen, id_producto, url_imagen, rol):
    validar_administrador(rol)

    validar_id(id_imagen, "ID de la imagen")
    validar_producto(id_producto)
    url_imagen = validar_url_imagen(url_imagen)

    buscar_imagen_negocio(id_imagen)

    try:
        resultado = actualizar_imagen_repo(
            id_imagen,
            id_producto,
            url_imagen
        )

        if not resultado:
            raise ValueError("No se pudo actualizar la imagen.")

        return True

    except IntegrityError:
        raise ValueError(
            "No se pudo actualizar la imagen. Verifica los datos ingresados."
        )


def eliminar_imagen_negocio(id_imagen, rol):
    validar_administrador(rol)

    buscar_imagen_negocio(id_imagen)

    resultado = eliminar_imagen_repo(id_imagen)

    if not resultado:
        raise ValueError("No se pudo eliminar la imagen.")

    return True
