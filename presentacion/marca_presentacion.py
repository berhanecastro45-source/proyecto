from prettytable import PrettyTable

from negocio.marca_negocio import (
    listar_marcas_negocio,
    listar_marcas_desactivadas_negocio,
    crear_marca_negocio,
    actualizar_marca_negocio,
    eliminar_marca_negocio,
    reactivar_marca_negocio
)


def solicitar_id():
    while True:
        texto = input("\nIngrese el ID de la marca: ").strip()

        if not texto.isdigit():
            print("[X] Debe ingresar un número entero válido.")
            continue

        id_marca = int(texto)

        if id_marca <= 0:
            print("[X] El ID debe ser un número positivo.")
            continue

        return id_marca


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


def mostrar_tabla_marcas(marcas, titulo):
    if not marcas:
        print("\n[X] No hay marcas para mostrar.")
        return False

    tabla = PrettyTable()
    tabla.field_names = ["ID", "Nombre"]

    for marca in marcas:
        tabla.add_row([
            marca.id_marca,
            marca.nombre
        ])

    print(f"\n--- {titulo} ---")
    print(tabla)

    return True


def obtener_marca_seleccionada(marcas):
    while True:
        id_marca = solicitar_id()

        for marca in marcas:
            if marca.id_marca == id_marca:
                return marca

        print("[X] El ID ingresado no pertenece al listado.")
        print("Ingrese un ID de la lista mostrada.")


def confirmar_operacion_marca(marca, accion):
    return solicitar_confirmacion(
        f"\n¿Está seguro de {accion} la marca "
        f"'{marca.nombre}'? (S/N): "
    )


def mostrar_marcas():
    try:
        marcas = listar_marcas_negocio()
        mostrar_tabla_marcas(marcas, "LISTADO DE MARCAS")
        return marcas

    except Exception:
        mostrar_error_general("Ocurrió un error al consultar las marcas.")
        return None


def mostrar_marcas_desactivadas(rol):
    try:
        marcas = listar_marcas_desactivadas_negocio(rol)

        mostrar_tabla_marcas(
            marcas,
            "MARCAS DESACTIVADAS"
        )

        return marcas

    except (ValueError, PermissionError) as e:
        mostrar_error(e)
        return None

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al consultar las marcas desactivadas."
        )
        return None


def registrar_marca(rol):
    print("\n--- REGISTRAR MARCA ---")

    try:
        nombre = input("Ingrese el nombre de la marca: ").strip()

        crear_marca_negocio(nombre, rol)

        print("\n[✔] Marca registrada correctamente.")

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al registrar la marca.")


def modificar_marca(rol):
    try:
        marcas = mostrar_marcas()

        if not marcas:
            return

        marca = obtener_marca_seleccionada(marcas)

        print(f"\n--- MODIFICAR MARCA: {marca.nombre} ---")
        print("Presione ENTER para conservar el nombre actual.")

        nombre = input(f"Nuevo nombre [{marca.nombre}]: ").strip()

        if not nombre:
            nombre = marca.nombre

        if nombre == marca.nombre:
            print("\nNo se realizaron cambios.")
            return

        actualizar_marca_negocio(
            marca.id_marca,
            nombre,
            rol
        )

        print("\n[✔] Marca actualizada correctamente.")

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al actualizar la marca.")


def desactivar_marca(rol):
    try:
        marcas = mostrar_marcas()

        if not marcas:
            return

        marca = obtener_marca_seleccionada(marcas)

        if not confirmar_operacion_marca(marca, "desactivar"):
            print("\nOperación cancelada.")
            return

        eliminar_marca_negocio(marca.id_marca, rol)

        print(
            f"\n[✔] Marca '{marca.nombre}' desactivada correctamente."
        )

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al desactivar la marca.")


def reactivar_marca(rol):
    try:
        marcas = mostrar_marcas_desactivadas(rol)

        if not marcas:
            return

        marca = obtener_marca_seleccionada(marcas)

        if not confirmar_operacion_marca(marca, "reactivar"):
            print("\nOperación cancelada.")
            return

        reactivar_marca_negocio(marca.id_marca, rol)

        print(
            f"\n[✔] Marca '{marca.nombre}' reactivada correctamente."
        )

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al reactivar la marca.")


def menu_marcas(rol):
    es_admin = (
        isinstance(rol, str)
        and rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n===== GESTIÓN DE MARCAS =====")
        print("1. Listar marcas")

        if es_admin:
            print("2. Registrar marca")
            print("3. Modificar marca")
            print("4. Desactivar marca")
            print("5. Listar marcas desactivadas")
            print("6. Reactivar marca")
            print("7. Volver")
        else:
            print("2. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            mostrar_marcas()

        elif opcion == "2" and es_admin:
            registrar_marca(rol)

        elif opcion == "3" and es_admin:
            modificar_marca(rol)

        elif opcion == "4" and es_admin:
            desactivar_marca(rol)

        elif opcion == "5" and es_admin:
            mostrar_marcas_desactivadas(rol)

        elif opcion == "6" and es_admin:
            reactivar_marca(rol)

        elif (opcion == "7" and es_admin) or (
            opcion == "2" and not es_admin
        ):
            break

        else:
            print("\n[X] Opción no válida o sin permisos.")


