from datos.modelos.categoria import Categoria


def listar_categorias_repo():
    return list(
        Categoria.select().where(Categoria.activo == 1)
    )


def listar_categorias_desactivadas_repo():
    return list(
        Categoria.select().where(Categoria.activo == 0)
    )


def obtener_categoria_por_id_repo(id_categoria):
    return Categoria.get_or_none(
        Categoria.id_categoria == id_categoria,
        Categoria.activo == 1
    )


def obtener_categoria_desactivada_por_id_repo(id_categoria):
    return Categoria.get_or_none(
        Categoria.id_categoria == id_categoria,
        Categoria.activo == 0
    )


def obtener_categoria_por_nombre_repo(nombre):
    return Categoria.get_or_none(
        Categoria.nombre == nombre
    )


def crear_categoria_repo(nombre, descripcion):
    objeto = Categoria(
        nombre=nombre,
        descripcion=descripcion,
        activo=1
    )
    objeto.save()
    return objeto


def actualizar_categoria_repo(id_categoria, nombre, descripcion):
    categoria = obtener_categoria_por_id_repo(id_categoria)

    if categoria is None:
        return False

    categoria.nombre = nombre
    categoria.descripcion = descripcion
    categoria.save()

    return True


def eliminar_categoria_repo(id_categoria):
    categoria = obtener_categoria_por_id_repo(id_categoria)

    if categoria is None:
        return False

    categoria.activo = 0
    categoria.save()

    return True


def reactivar_categoria_repo(id_categoria):
    categoria = obtener_categoria_desactivada_por_id_repo(id_categoria)

    if categoria is None:
        return False

    categoria.activo = 1
    categoria.save()

    return True
