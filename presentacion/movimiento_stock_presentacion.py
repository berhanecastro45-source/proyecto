
from prettytable import PrettyTable

from negocio.movimiento_stock_negocio import (
    listar_movimientos_negocio,
    listar_movimientos_por_producto_negocio,
    buscar_movimiento_negocio,
    registrar_movimiento_negocio
)

from negocio.producto_negocio import listar_productos_negocio


STOCK_MAXIMO = 2147483647


def solicitar_entero(mensaje, minimo=1, maximo=None):
    while True:
        try:
            valor = int(input(mensaje).strip())

            if valor < minimo:
                print(f"[X] El valor debe ser mayor o igual a {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"[X] El valor no puede ser mayor que {maximo}.")
                continue

            return valor

        except ValueError:
            print("[X] Debes ingresar un número entero válido.")


def presentar_tabla_movimientos(movimientos):
    if not movimientos:
        print("\nNo hay movimientos de stock registrados.")
        return False

    tabla = PrettyTable()
    tabla.field_names = [
        "ID movimiento",
        "ID producto",
        "Cantidad",
        "Tipo",
        "Fecha"
    ]

    for movimiento in movimientos:
        tabla.add_row([
            movimiento.id_movimiento,
            movimiento.id_producto,
            movimiento.cantidad,
            movimiento.tipo,
            movimiento.fecha_movimiento
        ])

    print(tabla)
    return True


def presentar_tabla_productos(productos):
    if not productos:
        print("\nNo hay productos activos disponibles.")
        return False

    tabla = PrettyTable()
    tabla.field_names = ["ID producto", "Nombre", "Stock"]

    for producto in productos:
        tabla.add_row([
            producto.id_producto,
            producto.nombre,
            producto.stock
        ])

    print("\n========== PRODUCTOS DISPONIBLES ==========")
    print(tabla)
    return True


def seleccionar_producto():
    productos = listar_productos_negocio()

    if not presentar_tabla_productos(productos):
        return None

    while True:
        id_producto = solicitar_entero(
            "\nIngrese el ID del producto: "
        )

        for producto in productos:
            if producto.id_producto == id_producto:
                return producto

        print(
            "[X] El ID no corresponde a un producto del listado. "
            "Intente nuevamente."
        )


def seleccionar_movimiento(movimientos):
    if not presentar_tabla_movimientos(movimientos):
        return None

    while True:
        id_movimiento = solicitar_entero(
            "\nIngrese el ID del movimiento: "
        )

        for movimiento in movimientos:
            if movimiento.id_movimiento == id_movimiento:
                return movimiento

        print(
            "[X] El ID no corresponde a un movimiento del listado. "
            "Intente nuevamente."
        )


def mostrar_detalle_movimiento(movimiento):
    tabla = PrettyTable()
    tabla.field_names = ["Campo", "Información"]
    tabla.add_row(["ID movimiento", movimiento.id_movimiento])
    tabla.add_row(["ID producto", movimiento.id_producto])
    tabla.add_row(["Cantidad", movimiento.cantidad])
    tabla.add_row(["Tipo", movimiento.tipo])
    tabla.add_row(["Fecha", movimiento.fecha_movimiento])

    print("\n========== INFORMACIÓN DEL MOVIMIENTO ==========")
    print(tabla)


def presentacion_listado_movimientos():
    try:
        movimientos = listar_movimientos_negocio()
        presentar_tabla_movimientos(movimientos)

    except Exception:
        print("\n[X] Ocurrió un error al listar los movimientos.")


def presentacion_movimientos_por_producto():
    try:
        producto = seleccionar_producto()

        if producto is None:
            return

        movimientos = listar_movimientos_por_producto_negocio(
            producto.id_producto
        )

        if not movimientos:
            print("\nEste producto no tiene movimientos registrados.")
            return

        print(
            f"\n========== MOVIMIENTOS DE "
            f"{producto.nombre.upper()} =========="
        )

        presentar_tabla_movimientos(movimientos)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print(
            "\n[X] Ocurrió un error al consultar "
            "los movimientos del producto."
        )


def presentacion_buscar_movimiento():
    try:
        movimientos = listar_movimientos_negocio()

        movimiento_seleccionado = seleccionar_movimiento(
            movimientos
        )

        if movimiento_seleccionado is None:
            return

        movimiento = buscar_movimiento_negocio(
            movimiento_seleccionado.id_movimiento
        )

        mostrar_detalle_movimiento(movimiento)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al buscar el movimiento.")


def solicitar_tipo_movimiento():
    while True:
        print("\n--- TIPOS DE MOVIMIENTO ---")
        print("1. ENTRADA")
        print("2. SALIDA")

        opcion = input(
            "Seleccione el tipo de movimiento: "
        ).strip()

        if opcion == "1":
            return "ENTRADA"

        elif opcion == "2":
            return "SALIDA"

        print("[X] Seleccione una opción válida (1 o 2).")


def solicitar_cantidad_movimiento(producto, tipo):
    if tipo == "SALIDA":
        if producto.stock <= 0:
            print(
                "[X] El producto no tiene stock disponible "
                "para realizar una salida."
            )
            return None

        maximo = producto.stock

    else:
        maximo = STOCK_MAXIMO - producto.stock

        if maximo <= 0:
            print(
                "[X] El stock del producto ya alcanzó "
                "el máximo permitido."
            )
            return None

    return solicitar_entero(
        f"Cantidad (máximo {maximo}): ",
        minimo=1,
        maximo=maximo
    )


def presentacion_registrar_movimiento(rol):
    print("\n========== REGISTRAR MOVIMIENTO DE STOCK ==========")

    if not isinstance(rol, str) or rol.strip().upper() != "ADMINISTRADOR":
        print(
            "\n[X] No tienes permisos para registrar "
            "movimientos de stock."
        )
        return

    try:
        producto = seleccionar_producto()

        if producto is None:
            return

        print(f"\nProducto seleccionado: {producto.nombre}")
        print(f"Stock actual: {producto.stock}")

        tipo = solicitar_tipo_movimiento()

        cantidad = solicitar_cantidad_movimiento(
            producto,
            tipo
        )

        if cantidad is None:
            return

        print("\nResumen del movimiento:")
        print(f"Producto: {producto.nombre}")
        print(f"Tipo: {tipo}")
        print(f"Cantidad: {cantidad}")

        if tipo == "ENTRADA":
            print(f"Stock resultante: {producto.stock + cantidad}")
        else:
            print(f"Stock resultante: {producto.stock - cantidad}")

        registrar_movimiento_negocio(
            producto.id_producto,
            cantidad,
            tipo,
            rol
        )

        print("\n[✔] Movimiento registrado correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print(
            "\n[X] Ocurrió un error al registrar "
            "el movimiento."
        )


def menu_movimiento_stock(usuario_actual):
    rol = usuario_actual.rol if usuario_actual else None

    es_administrador = (
        isinstance(rol, str)
        and rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n========== GESTIÓN DE STOCK ==========")
        print("1. Listar todos los movimientos")
        print("2. Consultar movimientos por producto")
        print("3. Buscar movimiento por ID")

        if es_administrador:
            print("4. Registrar movimiento")

        print("0. Volver al menú principal")

        opcion = input(
            "\nSeleccione una opción: "
        ).strip()

        if opcion == "1":
            presentacion_listado_movimientos()

        elif opcion == "2":
            presentacion_movimientos_por_producto()

        elif opcion == "3":
            presentacion_buscar_movimiento()

        elif opcion == "4" and es_administrador:
            presentacion_registrar_movimiento(rol)

        elif opcion == "0":
            break

        else:
            print(
                "\n[X] Opción inválida o no disponible "
                "para tu usuario."
            )

