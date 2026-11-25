from datos.modelos.cupon import Cupon


def listar_cupones_repo():
    return list(
        Cupon.select().where(Cupon.activo == 1)
    )


def obtener_cupon_por_id_repo(id_cupon):
    return Cupon.get_or_none(
        (Cupon.id_cupon == id_cupon) &
        (Cupon.activo == 1)
    )


def obtener_cupon_por_codigo_repo(codigo):
    return Cupon.get_or_none(
        Cupon.codigo == codigo
    )


def crear_cupon_repo(codigo, descuento, fecha_inicio, fecha_fin):
    objeto = Cupon(
        codigo=codigo,
        descuento=descuento,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_cupon_repo(
    id_cupon,
    codigo,
    descuento,
    fecha_inicio,
    fecha_fin
):
    cupon = obtener_cupon_por_id_repo(id_cupon)

    if cupon is None:
        return False

    cupon.codigo = codigo
    cupon.descuento = descuento
    cupon.fecha_inicio = fecha_inicio
    cupon.fecha_fin = fecha_fin

    cupon.save()
    return True


def eliminar_cupon_repo(id_cupon):
    cupon = obtener_cupon_por_id_repo(id_cupon)

    if cupon is None:
        return False

    cupon.activo = 0
    cupon.save()

    return True


def listar_cupones_desactivados_repo():
    return list(
        Cupon.select().where(Cupon.activo == 0)
    )


def obtener_cupon_desactivado_por_id_repo(id_cupon):
    return Cupon.get_or_none(
        (Cupon.id_cupon == id_cupon) &
        (Cupon.activo == 0)
    )


def reactivar_cupon_repo(id_cupon):
    cupon = obtener_cupon_desactivado_por_id_repo(id_cupon)

    if cupon is None:
        return False

    cupon.activo = 1
    cupon.save()

    return True


