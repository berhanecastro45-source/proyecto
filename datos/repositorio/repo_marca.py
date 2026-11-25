
from datos.modelos.marca import Marca


def obtener_marcas_repo(solo_activos=True):
    query = Marca.select()

    if solo_activos:
        query = query.where(Marca.activo == 1)

    return list(query)


def obtener_marcas_desactivadas_repo():
    return list(
        Marca.select().where(Marca.activo == 0)
    )


def obtener_marca_por_id_repo(id_marca):
    return Marca.get_or_none(
        (Marca.id_marca == id_marca) &
        (Marca.activo == 1)
    )


def obtener_marca_desactivada_por_id_repo(id_marca):
    return Marca.get_or_none(
        (Marca.id_marca == id_marca) &
        (Marca.activo == 0)
    )


def obtener_marca_por_nombre_repo(nombre):
    return Marca.get_or_none(
        Marca.nombre == nombre
    )


def crear_marca_repo(nombre):
    objeto = Marca(
        nombre=nombre,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_marca_repo(id_marca, nombre):
    marca = obtener_marca_por_id_repo(id_marca)

    if marca is None:
        return False

    marca.nombre = nombre
    marca.save()

    return True


def eliminar_marca_repo(id_marca):
    marca = obtener_marca_por_id_repo(id_marca)

    if marca is None:
        return False

    marca.activo = 0
    marca.save()

    return True


def reactivar_marca_repo(id_marca):
    marca = obtener_marca_desactivada_por_id_repo(id_marca)

    if marca is None:
        return False

    marca.activo = 1
    marca.save()

    return True
