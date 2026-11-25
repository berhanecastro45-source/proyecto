
from datos.modelos.usuario import Usuario


def guardar_usuario(rut, nombre, apellido_paterno, apellido_materno,
                    email, password_hash, telefono, fecha_nacimiento):

    objeto = Usuario(
        rut=rut,
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        email=email,
        password_hash=password_hash,
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento,
        rol="CLIENTE",
        activo=1
    )
    objeto.save()
    return objeto


def obtener_usuario_por_id(id_usuario):
    return Usuario.get_or_none(
        Usuario.id_usuario == id_usuario
    )


def obtener_usuario_por_email(email):
    return Usuario.get_or_none(
        (Usuario.email == email) & (Usuario.activo == 1)
    )


def obtener_usuario_por_email_registrado(email):
    return Usuario.get_or_none(
        Usuario.email == email
    )


def obtener_usuario_por_rut(rut):
    return Usuario.get_or_none(
        Usuario.rut == rut
    )


def obtener_usuario_por_rut_excluir(rut, id_usuario):
    return Usuario.get_or_none(
        (Usuario.rut == rut) & (Usuario.id_usuario != id_usuario)
    )


def actualizar_usuario_repo(id_usuario, datos):
    return Usuario.update(**datos).where(
        Usuario.id_usuario == id_usuario
    ).execute()


def desactivar_usuario_repo(id_usuario):
    return Usuario.update(activo=0).where(
        Usuario.id_usuario == id_usuario
    ).execute()


def listado_usuario():
    return list(
        Usuario.select().where(Usuario.activo == 1)
    )


def listar_usuarios_inactivos():
    return list(Usuario.select().where(Usuario.activo == 0))


def activar_usuario_repo(id_usuario):
    return Usuario.update(activo=1).where(
        Usuario.id_usuario == id_usuario
    ).execute()

def obtener_usuario_activo_por_id_repo(id_usuario):
    return Usuario.get_or_none(
        (Usuario.id_usuario == id_usuario) & (Usuario.activo == 1)
    )
