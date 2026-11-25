
from negocio.pedido_negocio import (
    obtener_historial_pedidos_negocio,
    procesar_checkout_negocio,
    cancelar_pedido_negocio
)


def solicitar_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje).strip())

            if valor < minimo:
                print(
                    f"[X] Debe ingresar un número mayor o igual a {minimo}."
                )
                continue

            return valor

        except ValueError:
            print("[X] Debe ingresar un número entero válido.")


def solicitar_direccion():
    while True:
        direccion = input(
            "Ingrese la dirección de envío: "
        ).strip()

        if direccion:
            return direccion

        print("[X] La dirección de envío no puede estar vacía.")


def mostrar_historial_pedidos_presentacion(usuario_actual):
    try:
        pedidos = obtener_historial_pedidos_negocio(usuario_actual)

        if not pedidos:
            print("\nNo tienes pedidos registrados.")
            return

        print("\n========== HISTORIAL DE PEDIDOS ==========")

        for pedido in pedidos:
            print(f"\nNúmero de pedido: {pedido.id_pedido}")
            print(f"Fecha: {pedido.fecha_pedido}")
            print(f"Estado: {pedido.estado}")
            print(f"Total: ${pedido.total}")
            print("------------------------------------------")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar el historial de pedidos.")


def checkout_presentacion(usuario_actual):
    try:
        print("\n========== FINALIZAR COMPRA ==========")

        direccion = solicitar_direccion()

        id_forma_pago = solicitar_entero(
            "Ingrese el ID de la forma de pago: "
        )

        codigo_cupon = input(
            "Ingrese el código del cupón (Enter si no tiene): "
        ).strip()

        if not codigo_cupon:
            codigo_cupon = None

        id_pedido = procesar_checkout_negocio(
            usuario_actual,
            direccion,
            id_forma_pago,
            codigo_cupon
        )

        print("\n[✔] ¡Pedido creado correctamente!")
        print(f"Número de pedido: {id_pedido}")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al finalizar la compra.")


def cancelar_pedido_presentacion(usuario_actual):
    try:
        id_pedido = solicitar_entero("ID del pedido a cancelar: ")
        cancelar_pedido_negocio(usuario_actual, id_pedido)
        print("\n[✔] Pedido cancelado correctamente. El stock fue devuelto.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] {error}")
