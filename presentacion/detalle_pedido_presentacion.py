
from prettytable import PrettyTable

from negocio.pedido_negocio import (
    listar_pedidos_disponibles_negocio
)

from negocio.detalle_pedido_negocio import (
    listar_detalles_pedido_negocio,
    obtener_detalle_pedido_negocio
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


def mostrar_tabla_pedidos(pedidos):

    if not pedidos:
        print("\nNo hay pedidos registrados.")
        return False

    tabla = PrettyTable()

    tabla.field_names = [
        "ID pedido",
        "ID usuario",
        "Estado",
        "Total"
    ]

    for pedido in pedidos:
        tabla.add_row([
            pedido.id_pedido,
            pedido.id_usuario,
            pedido.estado,
            f"${pedido.total}"
        ])

    print("\n========== PEDIDOS DISPONIBLES ==========")
    print(tabla)

    return True


def seleccionar_pedido(pedidos):

    if not mostrar_tabla_pedidos(pedidos):
        return None

    while True:
        id_pedido = solicitar_entero(
            "\nIngrese el ID del pedido: "
        )

        for pedido in pedidos:
            if pedido.id_pedido == id_pedido:
                return pedido

        print("[X] El ID no pertenece a los pedidos mostrados.")


def mostrar_tabla_detalles(detalles):

    if not detalles:
        print("\nEste pedido no tiene detalles registrados.")
        return False

    tabla = PrettyTable()

    tabla.field_names = [
        "ID detalle",
        "ID pedido",
        "ID producto",
        "Cantidad",
        "Precio unitario",
        "Subtotal"
    ]

    for detalle in detalles:
        tabla.add_row([
            detalle.id_detalle,
            detalle.id_pedido,
            detalle.id_producto,
            detalle.cantidad,
            f"${detalle.precio_unitario}",
            f"${detalle.subtotal}"
        ])

    print("\n========== DETALLES DEL PEDIDO ==========")
    print(tabla)

    return True


def mostrar_datos_detalle(detalle):

    tabla = PrettyTable()

    tabla.field_names = ["Campo", "Valor"]

    tabla.add_row(["ID detalle", detalle.id_detalle])
    tabla.add_row(["ID pedido", detalle.id_pedido])
    tabla.add_row(["ID producto", detalle.id_producto])
    tabla.add_row(["Cantidad", detalle.cantidad])
    tabla.add_row([
        "Precio unitario",
        f"${detalle.precio_unitario}"
    ])
    tabla.add_row(["Subtotal", f"${detalle.subtotal}"])

    print("\n========== DETALLE DEL PEDIDO ==========")
    print(tabla)


def obtener_pedidos_disponibles(usuario_actual):

    pedidos = listar_pedidos_disponibles_negocio(
        usuario_actual
    )

    return pedidos


def mostrar_detalles_pedido_presentacion(usuario_actual):

    try:
        pedidos = obtener_pedidos_disponibles(usuario_actual)

        pedido = seleccionar_pedido(pedidos)

        if pedido is None:
            return

        detalles = listar_detalles_pedido_negocio(
            usuario_actual,
            pedido.id_pedido
        )

        mostrar_tabla_detalles(detalles)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print(
            "\n[X] Ocurrió un error al consultar "
            "los detalles del pedido."
        )


def mostrar_detalle_pedido_presentacion(usuario_actual):

    try:
        pedidos = obtener_pedidos_disponibles(usuario_actual)

        pedido = seleccionar_pedido(pedidos)

        if pedido is None:
            return

        detalles = listar_detalles_pedido_negocio(
            usuario_actual,
            pedido.id_pedido
        )

        if not mostrar_tabla_detalles(detalles):
            return

        while True:
            id_detalle = solicitar_entero(
                "\nIngrese el ID del detalle que desea consultar: "
            )

            detalle_encontrado = None

            for detalle in detalles:
                if detalle.id_detalle == id_detalle:
                    detalle_encontrado = detalle
                    break

            if detalle_encontrado is not None:
                break

            print(
                "[X] El ID del detalle no pertenece "
                "al pedido seleccionado."
            )

        detalle = obtener_detalle_pedido_negocio(
            usuario_actual,
            detalle_encontrado.id_detalle
        )

        mostrar_datos_detalle(detalle)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print(
            "\n[X] Ocurrió un error al consultar "
            "el detalle del pedido."
        )
