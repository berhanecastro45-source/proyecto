from prettytable import PrettyTable

from negocio.pago_negocio import (
    listar_pagos_negocio,
    obtener_pago_negocio,
    listar_pagos_por_pedido_negocio,
    actualizar_estado_pago_negocio
)


def solicitar_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje).strip())

            if valor < minimo:
                print(f"[X] Debe ingresar un número mayor o igual a {minimo}.")
                continue

            return valor

        except ValueError:
            print("[X] Debe ingresar un número entero válido.")


def mostrar_tabla_pagos(pagos, titulo="LISTADO DE PAGOS"):
    if not pagos:
        print("\nNo hay pagos registrados.")
        return False

    tabla = PrettyTable()
    tabla.field_names = [
        "ID pago",
        "ID pedido",
        "ID forma de pago",
        "Monto",
        "Estado"
    ]

    for pago in pagos:
        tabla.add_row([
            pago.id_pago,
            pago.id_pedido,
            pago.id_forma_pago,
            f"${pago.monto}",
            pago.estado
        ])

    print(f"\n========== {titulo} ==========")
    print(tabla)
    return True


def obtener_pago_seleccionado(pagos):
    if not mostrar_tabla_pagos(pagos):
        return None

    while True:
        id_pago = solicitar_entero("\nIngrese el ID del pago: ")

        for pago in pagos:
            if pago.id_pago == id_pago:
                return pago

        print("[X] El ID ingresado no corresponde a un pago del listado.")


def mostrar_pagos_presentacion(usuario_actual):
    try:
        pagos = listar_pagos_negocio(usuario_actual)
        mostrar_tabla_pagos(pagos)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar los pagos.")


def mostrar_pago_presentacion(usuario_actual):
    try:
        if usuario_actual.rol == "ADMINISTRADOR":
            pagos = listar_pagos_negocio(usuario_actual)
            pago_seleccionado = obtener_pago_seleccionado(pagos)

            if pago_seleccionado is None:
                return

            id_pago = pago_seleccionado.id_pago
        else:
            id_pago = solicitar_entero("Ingrese el ID del pago: ")

        pago = obtener_pago_negocio(usuario_actual, id_pago)

        print("\n========== DETALLE DEL PAGO ==========")

        tabla = PrettyTable()
        tabla.field_names = ["Campo", "Información"]
        tabla.add_row(["ID del pago", pago.id_pago])
        tabla.add_row(["ID del pedido", pago.id_pedido])
        tabla.add_row(["ID forma de pago", pago.id_forma_pago])
        tabla.add_row(["Monto", f"${pago.monto}"])
        tabla.add_row(["Estado", pago.estado])

        print(tabla)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar el pago.")


def mostrar_pagos_por_pedido_presentacion(usuario_actual):
    try:
        id_pedido = solicitar_entero("Ingrese el ID del pedido: ")

        pagos = listar_pagos_por_pedido_negocio(
            usuario_actual,
            id_pedido
        )

        if not pagos:
            print("\nEste pedido no tiene pagos registrados.")
            return

        tabla = PrettyTable()
        tabla.field_names = ["ID pago", "Monto", "Estado"]

        for pago in pagos:
            tabla.add_row([
                pago.id_pago,
                f"${pago.monto}",
                pago.estado
            ])

        print("\n========== PAGOS DEL PEDIDO ==========")
        print(tabla)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar los pagos del pedido.")


def actualizar_estado_pago_presentacion(usuario_actual):
    try:
        pagos = listar_pagos_negocio(usuario_actual)
        pago = obtener_pago_seleccionado(pagos)

        if pago is None:
            return

        print("\nEstados disponibles:")
        print("1. PENDIENTE")
        print("2. APROBADO")
        print("3. RECHAZADO")

        while True:
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                estado = "PENDIENTE"
                break

            elif opcion == "2":
                estado = "APROBADO"
                break

            elif opcion == "3":
                estado = "RECHAZADO"
                break

            else:
                print("[X] Seleccione una opción válida (1, 2 o 3).")

        actualizar_estado_pago_negocio(
            usuario_actual,
            pago.id_pago,
            estado
        )

        print("\n[✔] ¡Estado del pago actualizado correctamente!")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al actualizar el estado del pago.")