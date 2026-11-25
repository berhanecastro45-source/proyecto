from prettytable import PrettyTable

from negocio.forma_pago_negocio import (
    listar_formas_pago_negocio,
    listar_formas_pago_desactivadas_negocio,
    obtener_forma_pago_negocio,
    crear_forma_pago_negocio,
    actualizar_forma_pago_negocio,
    desactivar_forma_pago_negocio,
    reactivar_forma_pago_negocio
)


def solicitar_id():
    while True:
        try:
            id_forma = int(
                input("Ingrese el ID de la forma de pago: ").strip()
            )

            if id_forma <= 0:
                print("[X] El ID debe ser un número positivo.")
                continue

            return id_forma

        except ValueError:
            print("[X] Debe ingresar un número entero válido.")


def solicitar_texto(mensaje, campo, maximo, valor_actual=None):
    while True:
        texto = input(mensaje).strip()

        if valor_actual is not None and not texto:
            return valor_actual

        if not texto:
            print(f"[X] {campo} es obligatorio.")
            continue

        if len(texto) > maximo:
            print(
                f"[X] {campo} no puede superar "
                f"los {maximo} caracteres."
            )
            continue

        return texto


def solicitar_confirmacion(mensaje):
    while True:
        confirmacion = input(mensaje).strip().upper()

        if confirmacion == "S":
            return True

        if confirmacion == "N":
            return False

        print("[X] Ingrese S para sí o N para no.")


def mostrar_tabla_formas_pago(formas, titulo):
    if not formas:
        print("\nNo hay formas de pago para mostrar.")
        return False

    tabla = PrettyTable()
    tabla.field_names = [
        "ID",
        "Nombre",
        "Descripción"
    ]

    for forma in formas:
        tabla.add_row([
            forma.id_forma_pago,
            forma.nombre,
            forma.descripcion
        ])

    print(f"\n========== {titulo} ==========")
    print(tabla)

    return True


def obtener_forma_seleccionada(formas):
    if not mostrar_tabla_formas_pago(
        formas,
        "FORMAS DE PAGO DISPONIBLES"
    ):
        return None

    while True:
        id_forma = solicitar_id()

        for forma in formas:
            if forma.id_forma_pago == id_forma:
                return forma

        print("[X] El ID no pertenece al listado mostrado.")


def mostrar_formas_pago_presentacion():
    try:
        formas = listar_formas_pago_negocio()

        mostrar_tabla_formas_pago(
            formas,
            "FORMAS DE PAGO ACTIVAS"
        )

    except Exception:
        print("\n[X] Ocurrió un error al listar las formas de pago.")


def mostrar_formas_pago_desactivadas_presentacion(rol):
    try:
        formas = listar_formas_pago_desactivadas_negocio(rol)

        mostrar_tabla_formas_pago(
            formas,
            "FORMAS DE PAGO DESACTIVADAS"
        )

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print(
            "\n[X] Ocurrió un error al listar "
            "las formas de pago desactivadas."
        )


def mostrar_forma_pago_presentacion():
    try:
        formas = listar_formas_pago_negocio()
        forma = obtener_forma_seleccionada(formas)

        if forma is None:
            return

        obtener_forma_pago_negocio(forma.id_forma_pago)

        print("\n========== FORMA DE PAGO ==========")
        print(f"ID: {forma.id_forma_pago}")
        print(f"Nombre: {forma.nombre}")
        print(f"Descripción: {forma.descripcion}")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar la forma de pago.")


def crear_forma_pago_presentacion(rol):
    print("\n========== REGISTRAR FORMA DE PAGO ==========")

    try:
        nombre = solicitar_texto(
            "Ingrese el nombre: ",
            "El nombre",
            100
        )

        descripcion = solicitar_texto(
            "Ingrese la descripción: ",
            "La descripción",
            255
        )

        crear_forma_pago_negocio(
            nombre,
            descripcion,
            rol
        )

        print("\n[✔] Forma de pago creada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al crear la forma de pago.")


def actualizar_forma_pago_presentacion(rol):
    print("\n========== ACTUALIZAR FORMA DE PAGO ==========")

    try:
        formas = listar_formas_pago_negocio()
        forma = obtener_forma_seleccionada(formas)

        if forma is None:
            return

        print("\nPresione ENTER para conservar el valor actual.")

        nombre = solicitar_texto(
            f"Nuevo nombre [{forma.nombre}]: ",
            "El nombre",
            100,
            forma.nombre
        )

        descripcion = solicitar_texto(
            f"Nueva descripción [{forma.descripcion}]: ",
            "La descripción",
            255,
            forma.descripcion
        )

        if (
            nombre == forma.nombre
            and descripcion == forma.descripcion
        ):
            print("\nNo se realizaron cambios.")
            return

        actualizar_forma_pago_negocio(
            forma.id_forma_pago,
            nombre,
            descripcion,
            rol
        )

        print("\n[✔] Forma de pago actualizada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al actualizar la forma de pago.")


def desactivar_forma_pago_presentacion(rol):
    print("\n========== DESACTIVAR FORMA DE PAGO ==========")

    try:
        formas = listar_formas_pago_negocio()
        forma = obtener_forma_seleccionada(formas)

        if forma is None:
            return

        confirmar = solicitar_confirmacion(
            f"\n¿Desea desactivar '{forma.nombre}'? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        desactivar_forma_pago_negocio(
            forma.id_forma_pago,
            rol
        )

        print("\n[✔] Forma de pago desactivada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al desactivar la forma de pago.")


def reactivar_forma_pago_presentacion(rol):
    print("\n========== REACTIVAR FORMA DE PAGO ==========")

    try:
        formas = listar_formas_pago_desactivadas_negocio(rol)
        forma = obtener_forma_seleccionada(formas)

        if forma is None:
            return

        confirmar = solicitar_confirmacion(
            f"\n¿Desea reactivar '{forma.nombre}'? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        reactivar_forma_pago_negocio(
            forma.id_forma_pago,
            rol
        )

        print("\n[✔] Forma de pago reactivada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al reactivar la forma de pago.")


def menu_formas_pago(rol):
    es_administrador = (
        isinstance(rol, str)
        and rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n========== MENÚ FORMAS DE PAGO ==========")
        print("1. Listar formas de pago")
        print("2. Buscar forma de pago por ID")

        if es_administrador:
            print("3. Crear forma de pago")
            print("4. Actualizar forma de pago")
            print("5. Desactivar forma de pago")
            print("6. Listar formas de pago desactivadas")
            print("7. Reactivar forma de pago")
            print("8. Volver")
        else:
            print("3. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            mostrar_formas_pago_presentacion()

        elif opcion == "2":
            mostrar_forma_pago_presentacion()

        elif es_administrador:
            if opcion == "3":
                crear_forma_pago_presentacion(rol)

            elif opcion == "4":
                actualizar_forma_pago_presentacion(rol)

            elif opcion == "5":
                desactivar_forma_pago_presentacion(rol)

            elif opcion == "6":
                mostrar_formas_pago_desactivadas_presentacion(rol)

            elif opcion == "7":
                reactivar_forma_pago_presentacion(rol)

            elif opcion == "8":
                break

            else:
                print("\n[X] Opción inválida.")

        elif opcion == "3":
            break

        else:
            print("\n[X] Opción inválida.")