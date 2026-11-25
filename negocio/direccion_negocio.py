from peewee import IntegrityError

from datos.repositorio.repo_direccion import (
    listado_direccion,
    listar_direcciones_por_usuario_repo,
    obtener_direccion_por_id_repo,
    crear_direccion_repo,
    actualizar_direccion_repo,
    eliminar_direccion_repo
)

from negocio.carrito_negocio import (
    validar_usuario_sesion,
    validar_administrador
)


def validar_id(id_registro, nombre="ID"):
    if (
        isinstance(id_registro, bool)
        or not isinstance(id_registro, int)
        or id_registro <= 0
    ):
        raise ValueError(f"{nombre} debe ser un número entero positivo.")


def validar_texto(valor, nombre, longitud):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{nombre} es obligatorio.")

    valor = valor.strip()

    if len(valor) > longitud:
        raise ValueError(f"{nombre} no puede superar los {longitud} caracteres.")

    return valor


def validar_datos_direccion(calle, ciudad, comuna, region, codigo_postal):
    calle = validar_texto(calle, "La calle", 150)
    ciudad = validar_texto(ciudad, "La ciudad", 100)
    comuna = validar_texto(comuna, "La comuna", 100)
    region = validar_texto(region, "La región", 100)

    if codigo_postal is not None and codigo_postal != "":
        codigo_postal = validar_texto(
            codigo_postal,
            "El código postal",
            20
        )
    else:
        codigo_postal = None

    return calle, ciudad, comuna, region, codigo_postal


def validar_direccion_propia(id_direccion, usuario_actual):
    validar_id(id_direccion, "El ID de la dirección")

    usuario = validar_usuario_sesion(usuario_actual)
    direccion = obtener_direccion_por_id_repo(id_direccion)

    if direccion is None or direccion.id_usuario != usuario.id_usuario:
        raise ValueError("La dirección no existe en tu cuenta.")

    return direccion


def listar_direcciones_negocio(usuario_actual):
    usuario = validar_usuario_sesion(usuario_actual)

    return listar_direcciones_por_usuario_repo(usuario.id_usuario)


def listar_todas_direcciones_negocio(usuario_actual):
    validar_administrador(usuario_actual)

    return listado_direccion()


def buscar_direccion_negocio(id_direccion, usuario_actual):
    return validar_direccion_propia(id_direccion, usuario_actual)


def crear_direccion_negocio(
    calle,
    ciudad,
    comuna,
    region,
    codigo_postal,
    usuario_actual
):
    usuario = validar_usuario_sesion(usuario_actual)

    datos = validar_datos_direccion(
        calle,
        ciudad,
        comuna,
        region,
        codigo_postal
    )

    try:
        return crear_direccion_repo(
            usuario.id_usuario,
            datos[0],
            datos[1],
            datos[2],
            datos[3],
            datos[4]
        )

    except IntegrityError:
        raise ValueError("No se pudo registrar la dirección.")


def actualizar_direccion_negocio(
    id_direccion,
    calle,
    ciudad,
    comuna,
    region,
    codigo_postal,
    usuario_actual
):
    validar_direccion_propia(id_direccion, usuario_actual)

    datos = validar_datos_direccion(
        calle,
        ciudad,
        comuna,
        region,
        codigo_postal
    )

    try:
        resultado = actualizar_direccion_repo(
            id_direccion,
            datos[0],
            datos[1],
            datos[2],
            datos[3],
            datos[4]
        )

        if not resultado:
            raise ValueError("No se pudo actualizar la dirección.")

        return True

    except IntegrityError:
        raise ValueError("No se pudo actualizar la dirección.")


def eliminar_direccion_negocio(id_direccion, usuario_actual):
    validar_direccion_propia(id_direccion, usuario_actual)

    resultado = eliminar_direccion_repo(id_direccion)

    if not resultado:
        raise ValueError("No se pudo desactivar la dirección.")

    return True
