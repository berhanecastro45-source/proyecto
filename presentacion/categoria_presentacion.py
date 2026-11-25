
from prettytable import PrettyTable

from negocio.categoria_negocio import (
    listar_categorias_negocio,
    listar_categorias_desactivadas_negocio,
    buscar_categoria_negocio,
    crear_categoria_negocio,
    actualizar_categoria_negocio,
    eliminar_categoria_negocio,
    reactivar_categoria_negocio,
    validar_nombre,
    validar_descripcion
)


def solicitar_id():
    while True:
        texto = input("Ingrese el ID de la categoría: ").strip()

        if not texto.isdigit():
            print("[X] Ingrese un ID numérico válido.")
            continue

        id_categoria = int(texto)

        if id_categoria <= 0:
            print("[X] El ID debe ser positivo.")
            continue

        return id_categoria


def solicitar_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()

        if respuesta == "s":
            return True

        if respuesta == "n":
            return False

        print("[X] Responda únicamente S o N.")


def mostrar_error(error):
    print(f"\n[X] Error: {error}")


def mostrar_error_general(mensaje):
    print(f"\n[X] {mensaje}")


def mostrar_tabla_categorias(categorias, titulo):
    if not categorias:
        print("\n[X] No hay categorías para mostrar.")
        return False

    tabla = PrettyTable()
    tabla.field_names = ["ID", "Nombre", "Descripción"]

    for categoria in categorias:
        tabla.add_row([
            categoria.id_categoria,
            categoria.nombre,
            categoria.descripcion
        ])

    print(f"\n--- {titulo} ---")
    print(tabla)

    return True


def obtener_categoria_seleccionada(categorias):
    while True:
        id_categoria = solicitar_id()

        for categoria in categorias:
            if categoria.id_categoria == id_categoria:
                return categoria

        print("[X] El ID ingresado no pertenece al listado.")
        print("Ingrese un ID de la lista mostrada.")


def solicitar_nombre(nombre_actual=None):
    while True:
        mensaje = "Ingrese el nombre de la categoría: "

        if nombre_actual is not None:
            mensaje = f"Nuevo nombre [{nombre_actual}]: "

        nombre = input(mensaje).strip()

        if not nombre and nombre_actual is not None:
            return nombre_actual

        try:
            return validar_nombre(nombre)

        except ValueError as error:
            mostrar_error(error)


def solicitar_descripcion(descripcion_actual=None):
    while True:
        mensaje = "Ingrese la descripción de la categoría: "

        if descripcion_actual is not None:
            mensaje = f"Nueva descripción [{descripcion_actual}]: "

        descripcion = input(mensaje).strip()

        if not descripcion and descripcion_actual is not None:
            return descripcion_actual

        try:
            return validar_descripcion(descripcion)

        except ValueError as error:
            mostrar_error(error)


def confirmar_operacion_categoria(categoria, accion):
    return solicitar_confirmacion(
        f"\n¿Está seguro de {accion} la categoría "
        f"'{categoria.nombre}'? (S/N): "
    )


def presentacion_listado_categoria():
    try:
        categorias = listar_categorias_negocio()

        mostrar_tabla_categorias(
            categorias,
            "LISTADO DE CATEGORÍAS"
        )

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al consultar las categorías."
        )


def presentacion_buscar_categoria():
    try:
        categorias = listar_categorias_negocio()

        if not mostrar_tabla_categorias(
            categorias,
            "CATEGORÍAS DISPONIBLES PARA CONSULTAR"
        ):
            return

        categoria_seleccionada = obtener_categoria_seleccionada(
            categorias
        )

        categoria = buscar_categoria_negocio(
            categoria_seleccionada.id_categoria
        )

        mostrar_tabla_categorias(
            [categoria],
            "INFORMACIÓN DE LA CATEGORÍA"
        )

    except ValueError as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al consultar la categoría."
        )


def presentacion_listado_categorias_desactivadas(rol):
    try:
        categorias = listar_categorias_desactivadas_negocio(rol)

        mostrar_tabla_categorias(
            categorias,
            "CATEGORÍAS DESACTIVADAS"
        )

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al consultar las categorías desactivadas."
        )


def presentacion_crear_categoria(rol):
    print("\n--- CREAR CATEGORÍA ---")

    try:
        nombre = solicitar_nombre()
        descripcion = solicitar_descripcion()

        crear_categoria_negocio(
            nombre,
            descripcion,
            rol
        )

        print("\n[✔] Categoría creada exitosamente.")

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al crear la categoría."
        )


def presentacion_actualizar_categoria(rol):
    try:
        categorias = listar_categorias_negocio()

        if not mostrar_tabla_categorias(
            categorias,
            "CATEGORÍAS DISPONIBLES PARA MODIFICAR"
        ):
            return

        categoria = obtener_categoria_seleccionada(categorias)

        print(f"\n--- MODIFICAR CATEGORÍA: {categoria.nombre} ---")
        print("Presione ENTER para conservar el dato actual.\n")

        nombre = solicitar_nombre(categoria.nombre)

        descripcion = solicitar_descripcion(
            categoria.descripcion
        )

        if (
            nombre == categoria.nombre
            and descripcion == categoria.descripcion
        ):
            print("\nNo se realizaron cambios.")
            return

        actualizar_categoria_negocio(
            categoria.id_categoria,
            nombre,
            descripcion,
            rol
        )

        print("\n[✔] Categoría actualizada exitosamente.")

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al actualizar la categoría."
        )


def presentacion_eliminar_categoria(rol):
    try:
        categorias = listar_categorias_negocio()

        if not mostrar_tabla_categorias(
            categorias,
            "CATEGORÍAS ACTIVAS PARA DESACTIVAR"
        ):
            return

        categoria = obtener_categoria_seleccionada(categorias)

        if not confirmar_operacion_categoria(categoria, "desactivar"):
            print("\nOperación cancelada.")
            return

        eliminar_categoria_negocio(
            categoria.id_categoria,
            rol
        )

        print(
            f"\n[✔] Categoría '{categoria.nombre}' "
            "desactivada exitosamente."
        )

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al desactivar la categoría."
        )


def presentacion_reactivar_categoria(rol):
    try:
        categorias = listar_categorias_desactivadas_negocio(rol)

        if not mostrar_tabla_categorias(
            categorias,
            "CATEGORÍAS DISPONIBLES PARA REACTIVAR"
        ):
            return

        categoria = obtener_categoria_seleccionada(categorias)

        if not confirmar_operacion_categoria(categoria, "reactivar"):
            print("\nOperación cancelada.")
            return

        reactivar_categoria_negocio(
            categoria.id_categoria,
            rol
        )

        print(
            f"\n[✔] Categoría '{categoria.nombre}' "
            "reactivada exitosamente."
        )

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al reactivar la categoría."
        )


def menu_categoria(usuario_actual):
    rol = usuario_actual.rol if usuario_actual else None

    es_admin = (
        isinstance(rol, str)
        and rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n--- MENÚ DE CATEGORÍAS ---")

        if es_admin:
            print("1. Listar categorías")
            print("2. Buscar categoría")
            print("3. Crear categoría")
            print("4. Actualizar categoría")
            print("5. Desactivar categoría")
            print("6. Listar categorías desactivadas")
            print("7. Reactivar categoría")
            print("8. Volver al menú principal")
        else:
            print("1. Listar categorías")
            print("2. Volver al menú principal")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            presentacion_listado_categoria()

        elif opcion == "2" and es_admin:
            presentacion_buscar_categoria()

        elif opcion == "3" and es_admin:
            presentacion_crear_categoria(rol)

        elif opcion == "4" and es_admin:
            presentacion_actualizar_categoria(rol)

        elif opcion == "5" and es_admin:
            presentacion_eliminar_categoria(rol)

        elif opcion == "6" and es_admin:
            presentacion_listado_categorias_desactivadas(rol)

        elif opcion == "7" and es_admin:
            presentacion_reactivar_categoria(rol)

        elif (opcion == "8" and es_admin) or (
            opcion == "2" and not es_admin
        ):
            break

        else:
            print("[X] Opción no válida o sin permisos.")
