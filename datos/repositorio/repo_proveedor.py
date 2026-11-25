from datos.modelos.proveedor import Proveedor


def listar_proveedores_repo():
    return list(
        Proveedor.select().where(Proveedor.activo == 1)
    )


def listar_proveedores_desactivados_repo():
    return list(
        Proveedor.select().where(Proveedor.activo == 0)
    )


def obtener_proveedor_por_id_repo(id_proveedor):
    return Proveedor.get_or_none(
        (Proveedor.id_proveedor == id_proveedor) &
        (Proveedor.activo == 1)
    )


def obtener_proveedor_desactivado_por_id_repo(id_proveedor):
    return Proveedor.get_or_none(
        (Proveedor.id_proveedor == id_proveedor) &
        (Proveedor.activo == 0)
    )


def obtener_proveedor_por_rut_repo(rut):
    return Proveedor.get_or_none(
        Proveedor.rut == rut
    )


def obtener_proveedor_por_email_repo(email):
    return Proveedor.get_or_none(
        Proveedor.email == email
    )


def crear_proveedor_repo(rut, nombre, telefono, email):
    objeto = Proveedor(
        rut=rut,
        nombre=nombre,
        telefono=telefono,
        email=email,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_proveedor_repo(id_proveedor, rut, nombre, telefono, email):
    proveedor = obtener_proveedor_por_id_repo(id_proveedor)

    if proveedor is None:
        return False

    proveedor.rut = rut
    proveedor.nombre = nombre
    proveedor.telefono = telefono
    proveedor.email = email
    proveedor.save()

    return True


def eliminar_proveedor_repo(id_proveedor):
    proveedor = obtener_proveedor_por_id_repo(id_proveedor)

    if proveedor is None:
        return False

    proveedor.activo = 0
    proveedor.save()

    return True


def reactivar_proveedor_repo(id_proveedor):
    proveedor = obtener_proveedor_desactivado_por_id_repo(id_proveedor)

    if proveedor is None:
        return False

    proveedor.activo = 1
    proveedor.save()

    return True
