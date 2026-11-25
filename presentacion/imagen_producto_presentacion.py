from prettytable import PrettyTable

from negocio.imagen_producto_negocio import (
    listar_imagenes_negocio,
    listar_imagenes_por_producto_negocio,
    buscar_imagen_negocio,
    crear_imagen_negocio,
    actualizar_imagen_negocio,
    eliminar_imagen_negocio
)


def solicitar_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje).strip())

            if valor < minimo:
                print(f"[X] El valor debe ser mayor o igual a {minimo}.")
                continue

            return valor

        except ValueError:
            print("[X] Debes ingresar un número entero válido.")


def solicitar_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()

        if respuesta == "s":
            return True

        if respuesta == "n":
            return False

        print("[X] Responde únicamente S o N.")


def presentar_tabla_imagenes(imagenes):
    if not imagenes:
        print("\nNo hay imágenes registradas.")
        return False

    tabla = PrettyTable()
    tabla.field_names = [
        "ID imagen",
        "ID producto",
        "URL de imagen"
    ]

    for imagen in imagenes:
        tabla.add_row([
            imagen.id_imagen,
            imagen.id_producto,
            imagen.url_imagen
        ])

    print(tabla)
    return True


def obtener_imagen_seleccionada(imagenes):
    while True:
        id_imagen = solicitar_entero(
            "\nIngrese el ID de la imagen: "
        )

        for imagen in imagenes:
            if imagen.id_imagen == id_imagen:
                return imagen

        print("[X] El ID no pertenece al listado.")


def presentacion_listado_imagenes():
    try:
        imagenes = listar_imagenes_negocio()

        presentar_tabla_imagenes(imagenes)

    except Exception:
        print("\n[X] Ocurrió un error al listar las imágenes.")


def presentacion_listado_por_producto():
    try:
        id_producto = solicitar_entero(
            "Ingrese el ID del producto: "
        )

        imagenes = listar_imagenes_por_producto_negocio(
            id_producto
        )

        if not imagenes:
            print("\nEste producto no tiene imágenes registradas.")
            return

        presentar_tabla_imagenes(imagenes)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print(
            "\n[X] Ocurrió un error al consultar "
            "las imágenes del producto."
        )


def presentacion_buscar_imagen():
    try:
        id_imagen = solicitar_entero(
            "Ingrese el ID de la imagen: "
        )

        imagen = buscar_imagen_negocio(id_imagen)

        print("\n--- INFORMACIÓN DE LA IMAGEN ---")
        print(f"ID: {imagen.id_imagen}")
        print(f"ID del producto: {imagen.id_producto}")
        print(f"URL: {imagen.url_imagen}")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al buscar la imagen.")


def presentacion_crear_imagen(rol):
    print("\n--- REGISTRAR IMAGEN ---")

    try:
        id_producto = solicitar_entero(
            "ID del producto: "
        )

        url_imagen = input(
            "URL o ruta de la imagen: "
        ).strip()

        crear_imagen_negocio(
            id_producto,
            url_imagen,
            rol
        )

        print("\n[✔] Imagen registrada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al registrar la imagen.")


def presentacion_actualizar_imagen(rol):
    print("\n--- ACTUALIZAR IMAGEN ---")

    try:
        imagenes = listar_imagenes_negocio()

        if not presentar_tabla_imagenes(imagenes):
            return

        imagen = obtener_imagen_seleccionada(imagenes)

        print("\nPresione ENTER para conservar el dato actual.")

        id_producto_texto = input(
            f"Nuevo ID del producto [{imagen.id_producto}]: "
        ).strip()

        if id_producto_texto:
            if not id_producto_texto.isdigit():
                print("[X] El ID del producto debe ser un entero positivo.")
                return

            id_producto = int(id_producto_texto)

            if id_producto <= 0:
                print("[X] El ID del producto debe ser positivo.")
                return
        else:
            id_producto = imagen.id_producto

        url_imagen = input(
            f"Nueva URL o ruta [{imagen.url_imagen}]: "
        ).strip()

        if not url_imagen:
            url_imagen = imagen.url_imagen

        if (
            id_producto == imagen.id_producto
            and url_imagen == imagen.url_imagen
        ):
            print("\nNo se realizaron cambios.")
            return

        actualizar_imagen_negocio(
            imagen.id_imagen,
            id_producto,
            url_imagen,
            rol
        )

        print("\n[✔] Imagen actualizada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al actualizar la imagen.")


def presentacion_eliminar_imagen(rol):
    print("\n--- DESACTIVAR IMAGEN ---")

    try:
        imagenes = listar_imagenes_negocio()

        if not presentar_tabla_imagenes(imagenes):
            return

        imagen = obtener_imagen_seleccionada(imagenes)

        confirmacion = solicitar_confirmacion(
            "\n¿Está seguro de que desea desactivar esta imagen? (S/N): "
        )

        if not confirmacion:
            print("\nOperación cancelada.")
            return

        eliminar_imagen_negocio(
            imagen.id_imagen,
            rol
        )

        print("\n[✔] Imagen desactivada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al desactivar la imagen.")


def menu_imagenes_producto(usuario_actual):
    rol = usuario_actual.rol if usuario_actual else None

    es_administrador = (
        isinstance(rol, str)
        and rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n========== GESTIÓN DE IMÁGENES ==========")
        print("1. Listar todas las imágenes")
        print("2. Consultar imágenes por producto")
        print("3. Buscar imagen por ID")

        if es_administrador:
            print("4. Registrar imagen")
            print("5. Actualizar imagen")
            print("6. Desactivar imagen")

        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            presentacion_listado_imagenes()

        elif opcion == "2":
            presentacion_listado_por_producto()

        elif opcion == "3":
            presentacion_buscar_imagen()

        elif opcion == "4" and es_administrador:
            presentacion_crear_imagen(rol)

        elif opcion == "5" and es_administrador:
            presentacion_actualizar_imagen(rol)

        elif opcion == "6" and es_administrador:
            presentacion_eliminar_imagen(rol)

        elif opcion == "0":
            break

        else:
            print("\n[X] Opción inválida o no disponible para tu usuario.")

