
from prettytable import PrettyTable

from negocio.carrito_negocio import (
    listar_carritos_negocio,
    buscar_carrito_negocio,
    buscar_carrito_por_usuario_negocio,
    obtener_carrito_propio_negocio,
    eliminar_carrito_negocio
)


def solicitar_entero(mensaje, minimo=1):
    while True:
        texto = input(mensaje).strip()

        if not texto.isdigit():
            print("[X] Debe ingresar un número entero válido.")
            continue

        valor = int(texto)

        if valor < minimo:
            print(
                f"[X] Debe ingresar un número mayor o igual a {minimo}."
            )
            continue

        return valor


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


def presentar_tabla_carritos(carritos, titulo="LISTADO DE CARRITOS"):
    if not carritos:
        print("\n[X] No hay carritos para mostrar.")
        return False

    tabla = PrettyTable()

    tabla.field_names = [
        "ID carrito",
        "ID usuario",
        "Estado"
    ]

    for carrito in carritos:
        estado = "Activo" if carrito.activo == 1 else "Inactivo"

        tabla.add_row([
            carrito.id_carrito,
            carrito.id_usuario,
            estado
        ])

    print(f"\n--- {titulo} ---")
    print(tabla)

    return True


def obtener_carrito_seleccionado(carritos):
    while True:
        id_carrito = solicitar_entero(
            "Ingrese el ID del carrito: "
        )

        for carrito in carritos:
            if carrito.id_carrito == id_carrito:
                return carrito

        print("[X] El ID ingresado no pertenece al listado.")
        print("Ingrese un ID de carrito de la tabla mostrada.")


def obtener_id_usuario_seleccionado(carritos):
    while True:
        id_usuario = solicitar_entero(
            "Ingrese el ID del usuario: "
        )

        for carrito in carritos:
            if carrito.id_usuario == id_usuario:
                return id_usuario

        print("[X] El usuario no aparece en el listado de carritos.")
        print("Ingrese un ID de usuario de la tabla mostrada.")


def presentacion_listado_carritos(usuario_actual):
    try:
        carritos = listar_carritos_negocio(usuario_actual)

        presentar_tabla_carritos(
            carritos,
            "LISTADO DE TODOS LOS CARRITOS"
        )

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al listar los carritos."
        )


def presentacion_buscar_carrito(usuario_actual):
    try:
        carritos = listar_carritos_negocio(usuario_actual)

        if not presentar_tabla_carritos(
            carritos,
            "CARRITOS DISPONIBLES PARA CONSULTAR"
        ):
            return

        carrito_seleccionado = obtener_carrito_seleccionado(
            carritos
        )

        carrito = buscar_carrito_negocio(
            carrito_seleccionado.id_carrito,
            usuario_actual
        )

        presentar_tabla_carritos(
            [carrito],
            "INFORMACIÓN DEL CARRITO"
        )

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al buscar el carrito."
        )


def presentacion_buscar_carrito_usuario(usuario_actual):
    try:
        carritos = listar_carritos_negocio(usuario_actual)

        if not presentar_tabla_carritos(
            carritos,
            "CARRITOS Y SUS USUARIOS"
        ):
            return

        id_usuario = obtener_id_usuario_seleccionado(carritos)

        carrito = buscar_carrito_por_usuario_negocio(
            id_usuario,
            usuario_actual
        )

        presentar_tabla_carritos(
            [carrito],
            "CARRITO DEL USUARIO"
        )

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al buscar el carrito del usuario."
        )


def presentacion_mi_carrito(usuario_actual):
    try:
        carrito = obtener_carrito_propio_negocio(usuario_actual)

        presentar_tabla_carritos(
            [carrito],
            "MI CARRITO"
        )

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al obtener tu carrito."
        )


def presentacion_eliminar_carrito(usuario_actual):
    try:
        carritos = listar_carritos_negocio(usuario_actual)

        if not presentar_tabla_carritos(
            carritos,
            "CARRITOS DISPONIBLES PARA DESACTIVAR"
        ):
            return

        carrito = obtener_carrito_seleccionado(carritos)

        confirmar = solicitar_confirmacion(
            f"\n¿Está seguro de desactivar el carrito "
            f"con ID {carrito.id_carrito}? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        eliminar_carrito_negocio(
            carrito.id_carrito,
            usuario_actual
        )

        print("\n[✔] Carrito desactivado correctamente.")

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al desactivar el carrito."
        )


def menu_carrito(usuario_actual):
    rol = usuario_actual.rol if usuario_actual else None

    es_administrador = (
        isinstance(rol, str)
        and rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n--- GESTIÓN DE CARRITOS ---")

        if es_administrador:
            print("1. Listar todos los carritos")
            print("2. Buscar carrito por ID")
            print("3. Buscar carrito por usuario")
            print("4. Desactivar carrito")
        else:
            print("1. Consultar mi carrito")

        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            if es_administrador:
                presentacion_listado_carritos(usuario_actual)
            else:
                presentacion_mi_carrito(usuario_actual)

        elif opcion == "2" and es_administrador:
            presentacion_buscar_carrito(usuario_actual)

        elif opcion == "3" and es_administrador:
            presentacion_buscar_carrito_usuario(usuario_actual)

        elif opcion == "4" and es_administrador:
            presentacion_eliminar_carrito(usuario_actual)

        elif opcion == "0":
            break

        else:
            print("\n[X] Opción inválida o sin permisos.")
