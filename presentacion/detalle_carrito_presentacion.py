
from prettytable import PrettyTable

from negocio.detalle_carrito_negocio import (
    listar_detalles_carrito_negocio,
    buscar_detalle_carrito_negocio,
    agregar_producto_carrito_negocio,
    actualizar_cantidad_detalle_negocio,
    eliminar_producto_carrito_negocio
)

from negocio.producto_negocio import (
    listar_productos_negocio
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


def presentar_tabla_detalles(detalles):
    if not detalles:
        print("\nTu carrito no contiene productos.")
        return False

    tabla = PrettyTable()

    tabla.field_names = [
        "ID detalle",
        "ID producto",
        "Cantidad",
        "Precio unitario",
        "Subtotal"
    ]

    for detalle in detalles:
        tabla.add_row([
            detalle.id_detalle_carrito,
            detalle.id_producto,
            detalle.cantidad,
            f"${detalle.precio_unitario}",
            f"${detalle.subtotal}"
        ])

    print("\n========== PRODUCTOS DE TU CARRITO ==========")
    print(tabla)

    return True


def presentar_tabla_productos(productos):
    if not productos:
        print("\nNo hay productos disponibles.")
        return False

    tabla = PrettyTable()

    tabla.field_names = [
        "ID producto",
        "Nombre",
        "Precio",
        "Stock disponible"
    ]

    for producto in productos:
        tabla.add_row([
            producto.id_producto,
            producto.nombre,
            f"${producto.precio}",
            producto.stock
        ])

    print("\n========== PRODUCTOS DISPONIBLES ==========")
    print(tabla)

    return True


def obtener_detalle_seleccionado(detalles):
    while True:
        id_detalle = solicitar_entero(
            "\nIngrese el ID del detalle: "
        )

        for detalle in detalles:
            if detalle.id_detalle_carrito == id_detalle:
                return detalle

        print("[X] El ID no pertenece a los productos de tu carrito.")


def obtener_producto_seleccionado(productos):
    while True:
        id_producto = solicitar_entero(
            "\nIngrese el ID del producto: "
        )

        for producto in productos:
            if producto.id_producto == id_producto:
                return producto

        print("[X] El ID no pertenece a los productos disponibles.")


def solicitar_cantidad():
    return solicitar_entero(
        "Ingrese la cantidad: "
    )


def presentacion_listado_detalles(usuario_actual):
    try:
        detalles = listar_detalles_carrito_negocio(usuario_actual)

        presentar_tabla_detalles(detalles)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print(
            "\n[X] Ocurrió un error al listar "
            "los productos del carrito."
        )


def presentacion_buscar_detalle(usuario_actual):
    try:
        detalles = listar_detalles_carrito_negocio(usuario_actual)

        if not presentar_tabla_detalles(detalles):
            return

        detalle_seleccionado = obtener_detalle_seleccionado(detalles)

        detalle = buscar_detalle_carrito_negocio(
            detalle_seleccionado.id_detalle_carrito,
            usuario_actual
        )

        presentar_tabla_detalles([detalle])

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al buscar el detalle.")


def presentacion_agregar_producto(usuario_actual):
    try:
        print("\n--- AGREGAR PRODUCTO AL CARRITO ---")

        productos = listar_productos_negocio()

        if not presentar_tabla_productos(productos):
            return

        producto = obtener_producto_seleccionado(productos)

        cantidad = solicitar_cantidad()

        agregar_producto_carrito_negocio(
            producto.id_producto,
            cantidad,
            usuario_actual
        )

        print("\n[✔] Producto agregado al carrito correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al agregar el producto.")


def presentacion_actualizar_cantidad(usuario_actual):
    try:
        detalles = listar_detalles_carrito_negocio(usuario_actual)

        if not presentar_tabla_detalles(detalles):
            return

        detalle = obtener_detalle_seleccionado(detalles)

        while True:
            cantidad = solicitar_cantidad()

            if cantidad == detalle.cantidad:
                print(
                    "\nLa cantidad ingresada es igual a la actual."
                )
                continue

            try:
                actualizar_cantidad_detalle_negocio(
                    detalle.id_detalle_carrito,
                    cantidad,
                    usuario_actual
                )

                print("\n[✔] Cantidad actualizada correctamente.")
                break

            except ValueError as error:
                print(f"\n[X] Error: {error}")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al actualizar la cantidad.")


def presentacion_eliminar_producto(usuario_actual):
    try:
        detalles = listar_detalles_carrito_negocio(usuario_actual)

        if not presentar_tabla_detalles(detalles):
            return

        detalle = obtener_detalle_seleccionado(detalles)

        confirmar = input(
            "\n¿Está seguro de eliminar este producto del carrito? (S/N): "
        ).strip().lower()

        while confirmar not in ("s", "n"):
            print("[X] Responda únicamente S o N.")

            confirmar = input(
                "¿Está seguro de eliminar este producto? (S/N): "
            ).strip().lower()

        if confirmar == "n":
            print("\nOperación cancelada.")
            return

        eliminar_producto_carrito_negocio(
            detalle.id_detalle_carrito,
            usuario_actual
        )

        print("\n[✔] Producto eliminado del carrito correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al eliminar el producto.")


def menu_detalle_carrito(usuario_actual):
    while True:
        print("\n--- MI CARRITO ---")
        print("1. Ver mis productos")
        print("2. Buscar detalle por ID")
        print("3. Agregar producto")
        print("4. Actualizar cantidad")
        print("5. Eliminar producto")
        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            presentacion_listado_detalles(usuario_actual)

        elif opcion == "2":
            presentacion_buscar_detalle(usuario_actual)

        elif opcion == "3":
            presentacion_agregar_producto(usuario_actual)

        elif opcion == "4":
            presentacion_actualizar_cantidad(usuario_actual)

        elif opcion == "5":
            presentacion_eliminar_producto(usuario_actual)

        elif opcion == "0":
            break

        else:
            print("\n[X] Opción inválida.")
