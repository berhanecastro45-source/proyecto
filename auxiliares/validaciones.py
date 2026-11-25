"""Validaciones y mensajes reutilizables por todas las capas."""

MSG_SIN_PERMISOS = "No tienes permisos para realizar esta operación."
MSG_OPCION_INVALIDA = "Opción no válida."
ROL_ADMINISTRADOR = "ADMINISTRADOR"


def rol_es_administrador(rol):
    """True si el rol (texto) corresponde a un administrador."""
    return isinstance(rol, str) and rol.strip().upper() == ROL_ADMINISTRADOR


def es_administrador(usuario):
    """True si el usuario (objeto con atributo rol) es administrador."""
    return usuario is not None and rol_es_administrador(getattr(usuario, "rol", None))


def validar_administrador(rol):
    """Lanza PermissionError si el rol no es administrador."""
    if not rol_es_administrador(rol):
        raise PermissionError(MSG_SIN_PERMISOS)


def validar_entero_positivo(valor, nombre="ID"):
    """Lanza ValueError si valor no es un entero positivo (excluye bool)."""
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise ValueError(f"El {nombre} debe ser un número entero positivo.")
