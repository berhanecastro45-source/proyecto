from datetime import date
from decimal import Decimal, InvalidOperation
from peewee import IntegrityError

from datos.repositorio.repo_usuario import obtener_usuario_activo_por_id_repo
from datos.repositorio.repo_cupon import (
    listar_cupones_repo,
    listar_cupones_desactivados_repo,
    obtener_cupon_por_id_repo,
    obtener_cupon_desactivado_por_id_repo,
    obtener_cupon_por_codigo_repo,
    crear_cupon_repo,
    actualizar_cupon_repo,
    eliminar_cupon_repo,
    reactivar_cupon_repo
)

def validar_administrador(usuario_actual):
    if usuario_actual is None:
        raise PermissionError("Debes iniciar sesión.")

    id_usuario = getattr(usuario_actual, "id_usuario", None)

    if isinstance(id_usuario, bool) or not isinstance(id_usuario, int) or id_usuario <= 0:
        raise PermissionError("La sesión de usuario no es válida.")

    usuario = obtener_usuario_activo_por_id_repo(id_usuario)

    if usuario is None or usuario.rol.strip().upper() != "ADMINISTRADOR":
        raise PermissionError("No tienes permisos para administrar cupones.")

    return usuario


def validar_id(id_cupon):
    if isinstance(id_cupon, bool) or not str(id_cupon).isdigit():
        raise ValueError("El ID del cupón debe ser un número entero positivo.")

    id_cupon = int(id_cupon)

    if id_cupon <= 0:
        raise ValueError("El ID del cupón debe ser mayor que cero.")

    return id_cupon


def validar_codigo(codigo):
    if not isinstance(codigo, str):
        raise ValueError("El código del cupón debe ser texto.")

    codigo = codigo.strip().upper()

    if not codigo or len(codigo) > 50:
        raise ValueError("El código debe tener entre 1 y 50 caracteres.")

    return codigo


def validar_descuento(descuento):
    try:
        descuento = Decimal(str(descuento))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("El descuento debe ser un número válido.")

    if not descuento.is_finite() or descuento <= 0 or descuento > 100:
        raise ValueError("El descuento debe ser mayor que 0 y menor o igual a 100.")

    if descuento.as_tuple().exponent < -2:
        raise ValueError("El descuento admite como máximo dos decimales.")

    return descuento


def validar_fecha(fecha, nombre):
    if isinstance(fecha, date):
        return fecha

    try:
        return date.fromisoformat(str(fecha).strip())
    except (ValueError, TypeError):
        raise ValueError(f"La {nombre} debe tener el formato AAAA-MM-DD.")


def validar_fechas(fecha_inicio, fecha_fin):
    fecha_inicio = validar_fecha(fecha_inicio, "fecha de inicio")
    fecha_fin = validar_fecha(fecha_fin, "fecha de término")

    if fecha_fin < fecha_inicio:
        raise ValueError("La fecha de término no puede ser anterior a la fecha de inicio.")

    return fecha_inicio, fecha_fin


def listar_cupones_negocio(usuario_actual):
    validar_administrador(usuario_actual)
    return listar_cupones_repo()



def listar_cupones_desactivados_negocio(usuario_actual):
    validar_administrador(usuario_actual)

    return listar_cupones_desactivados_repo()


def reactivar_cupon_negocio(id_cupon, usuario_actual):
    validar_administrador(usuario_actual)

    id_cupon = validar_id(id_cupon)

    cupon = obtener_cupon_desactivado_por_id_repo(id_cupon)

    if cupon is None:
        raise ValueError("El cupón no existe o ya está activo.")

    if not reactivar_cupon_repo(id_cupon):
        raise ValueError("No se pudo reactivar el cupón.")

    return True


def buscar_cupon_negocio(id_cupon, usuario_actual):
    validar_administrador(usuario_actual)
    id_cupon = validar_id(id_cupon)

    cupon = obtener_cupon_por_id_repo(id_cupon)

    if cupon is None:
        raise ValueError("El cupón no existe o está inactivo.")

    return cupon


def crear_cupon_negocio(codigo, descuento, fecha_inicio, fecha_fin, usuario_actual):
    validar_administrador(usuario_actual)

    codigo = validar_codigo(codigo)
    descuento = validar_descuento(descuento)
    fecha_inicio, fecha_fin = validar_fechas(fecha_inicio, fecha_fin)

    if obtener_cupon_por_codigo_repo(codigo):
        raise ValueError("Ya existe un cupón con ese código.")

    try:
        return crear_cupon_repo(
            codigo,
            descuento,
            fecha_inicio,
            fecha_fin
        )
    except IntegrityError:
        raise ValueError("No se pudo registrar el cupón porque el código ya existe.")


def actualizar_cupon_negocio(
    id_cupon,
    codigo,
    descuento,
    fecha_inicio,
    fecha_fin,
    usuario_actual
):
    validar_administrador(usuario_actual)

    id_cupon = validar_id(id_cupon)
    codigo = validar_codigo(codigo)
    descuento = validar_descuento(descuento)
    fecha_inicio, fecha_fin = validar_fechas(fecha_inicio, fecha_fin)

    cupon = obtener_cupon_por_id_repo(id_cupon)

    if cupon is None:
        raise ValueError("El cupón no existe o está inactivo.")

    otro_cupon = obtener_cupon_por_codigo_repo(codigo)

    if otro_cupon is not None and otro_cupon.id_cupon != id_cupon:
        raise ValueError("Ese código ya está siendo utilizado por otro cupón.")

    try:
        if not actualizar_cupon_repo(
            id_cupon,
            codigo,
            descuento,
            fecha_inicio,
            fecha_fin
        ):
            raise ValueError("No se pudo actualizar el cupón.")

        return obtener_cupon_por_id_repo(id_cupon)

    except IntegrityError:
        raise ValueError("No se pudo actualizar el cupón porque el código ya existe.")


def eliminar_cupon_negocio(id_cupon, usuario_actual):
    validar_administrador(usuario_actual)

    id_cupon = validar_id(id_cupon)

    if obtener_cupon_por_id_repo(id_cupon) is None:
        raise ValueError("El cupón no existe o ya está inactivo.")

    if not eliminar_cupon_repo(id_cupon):
        raise ValueError("No se pudo desactivar el cupón.")

    return True


