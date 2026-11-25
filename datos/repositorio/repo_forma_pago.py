from datos.modelos.forma_pago import FormaPago


def listar_formas_pago_repo():
    return list(
        FormaPago.select().where(
            FormaPago.activo == 1
        )
    )


def listar_formas_pago_desactivadas_repo():
    return list(
        FormaPago.select().where(
            FormaPago.activo == 0
        )
    )


def obtener_forma_pago_por_id_repo(id_forma_pago):
    return FormaPago.get_or_none(
        (FormaPago.id_forma_pago == id_forma_pago)
        & (FormaPago.activo == 1)
    )


def obtener_forma_pago_desactivada_por_id_repo(id_forma_pago):
    return FormaPago.get_or_none(
        (FormaPago.id_forma_pago == id_forma_pago)
        & (FormaPago.activo == 0)
    )


def crear_forma_pago_repo(nombre, descripcion):
    objeto = FormaPago(
        nombre=nombre,
        descripcion=descripcion,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_forma_pago_repo(id_forma_pago, nombre, descripcion):
    forma_pago = obtener_forma_pago_por_id_repo(id_forma_pago)

    if forma_pago is None:
        return False

    forma_pago.nombre = nombre
    forma_pago.descripcion = descripcion

    return forma_pago.save() > 0


def obtener_forma_pago_por_nombre_repo(nombre):
    return FormaPago.get_or_none(
        FormaPago.nombre == nombre
    )


def desactivar_forma_pago_repo(id_forma_pago):
    forma_pago = obtener_forma_pago_por_id_repo(id_forma_pago)

    if forma_pago is None:
        return False

    forma_pago.activo = 0

    return forma_pago.save() > 0


def reactivar_forma_pago_repo(id_forma_pago):
    forma_pago = obtener_forma_pago_desactivada_por_id_repo(id_forma_pago)

    if forma_pago is None:
        return False

    forma_pago.activo = 1

    return forma_pago.save() > 0


