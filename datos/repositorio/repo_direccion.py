
from datos.modelos.direccion import Direccion


def listado_direccion():
    return list(Direccion.select())


def listar_direcciones_por_usuario_repo(id_usuario):
    return list(
        Direccion.select().where(
            (Direccion.id_usuario == id_usuario) &
            (Direccion.activo == 1)
        )
    )


def obtener_direccion_por_id_repo(id_direccion):
    return Direccion.get_or_none(
        (Direccion.id_direccion == id_direccion) &
        (Direccion.activo == 1)
    )


def crear_direccion_repo(id_usuario, calle, ciudad, comuna, region, codigo_postal=None):
    objeto = Direccion(
        id_usuario=id_usuario,
        calle=calle,
        ciudad=ciudad,
        comuna=comuna,
        region=region,
        codigo_postal=codigo_postal,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_direccion_repo(id_direccion, calle, ciudad, comuna, region, codigo_postal=None):
    direccion = obtener_direccion_por_id_repo(id_direccion)

    if direccion is None:
        return False

    direccion.calle = calle
    direccion.ciudad = ciudad
    direccion.comuna = comuna
    direccion.region = region
    direccion.codigo_postal = codigo_postal

    direccion.save()
    return True


def eliminar_direccion_repo(id_direccion):
    direccion = obtener_direccion_por_id_repo(id_direccion)

    if direccion is None:
        return False

    direccion.activo = 0
    direccion.save()

    return True
