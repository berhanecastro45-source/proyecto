from auxiliares.validaciones import es_administrador

from datos.conexion import DB

from presentacion.usuario_presentacion import (
    procesar_login as procesar_login_presentacion,
    menu_usuarios
)

from presentacion.categoria_presentacion import menu_categoria
from presentacion.marca_presentacion import menu_marcas
from presentacion.proveedor_presentacion import menu_proveedores
from presentacion.producto_presentacion import menu_productos
from presentacion.imagen_producto_presentacion import menu_imagenes_producto
from presentacion.movimiento_stock_presentacion import menu_movimiento_stock
from presentacion.cupon_presentacion import menu_cupones
from presentacion.forma_pago_presentacion import menu_formas_pago
from presentacion.direccion_presentacion import menu_direccion
from presentacion.carrito_presentacion import menu_carrito
from presentacion.detalle_carrito_presentacion import menu_detalle_carrito
from presentacion.valoracion_presentacion import menu_valoracion

from presentacion.pedido_presentacion import (
    mostrar_historial_pedidos_presentacion,
    checkout_presentacion,
    cancelar_pedido_presentacion
)

from presentacion.detalle_pedido_presentacion import (
    mostrar_detalles_pedido_presentacion,
    mostrar_detalle_pedido_presentacion
)

from presentacion.pago_presentacion import (
    mostrar_pagos_presentacion,
    mostrar_pago_presentacion,
    mostrar_pagos_por_pedido_presentacion,
    actualizar_estado_pago_presentacion
)


usuario_en_sesion = None


TODOS = "todos"
ADMIN = "admin"
CLIENTE = "cliente"


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def abrir_menu_marcas(usuario):
    menu_marcas(usuario.rol)


def abrir_menu_formas_pago(usuario):
    menu_formas_pago(usuario.rol)


def filtrar_opciones(opciones, es_admin):
    opciones_visibles = []

    for opcion in opciones:
        if opcion[2] == TODOS:
            opciones_visibles.append(opcion)

        elif opcion[2] == ADMIN and es_admin:
            opciones_visibles.append(opcion)

        elif opcion[2] == CLIENTE and not es_admin:
            opciones_visibles.append(opcion)

    return opciones_visibles


def mostrar_submenu(titulo, opciones, usuario):
    opciones_visibles = filtrar_opciones(
        opciones,
        es_administrador(usuario)
    )

    while True:
        print(f"\n--- {titulo} ---")

        numero = 1

        for opcion in opciones_visibles:
            print(f"{numero}. {opcion[0]}")
            numero += 1

        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "0":
            break

        if opcion.isdigit():
            numero = int(opcion)

            if 1 <= numero <= len(opciones_visibles):
                opciones_visibles[numero - 1][1](usuario)
            else:
                print("\n[X] Opción no válida.")
        else:
            print("\n[X] Opción no válida.")


# ---------------------------------------------------------------------------
# Submenú de pedidos
# ---------------------------------------------------------------------------

def menu_pedidos(usuario_actual):
    opciones = [
        (
            "Ver historial de pedidos",
            mostrar_historial_pedidos_presentacion,
            TODOS
        ),
        (
            "Finalizar compra",
            checkout_presentacion,
            CLIENTE
        ),
        (
            "Cancelar pedido pendiente",
            cancelar_pedido_presentacion,
            TODOS
        ),
        (
            "Ver detalles de un pedido",
            mostrar_detalles_pedido_presentacion,
            TODOS
        ),
        (
            "Buscar detalle de pedido por ID",
            mostrar_detalle_pedido_presentacion,
            TODOS
        )
    ]

    mostrar_submenu(
        "GESTIÓN DE PEDIDOS",
        opciones,
        usuario_actual
    )


# ---------------------------------------------------------------------------
# Submenú de pagos
# ---------------------------------------------------------------------------

def menu_pagos(usuario_actual):
    opciones = [
        (
            "Buscar pago por ID",
            mostrar_pago_presentacion,
            TODOS
        ),
        (
            "Ver pagos de un pedido",
            mostrar_pagos_por_pedido_presentacion,
            TODOS
        ),
        (
            "Listar todos los pagos",
            mostrar_pagos_presentacion,
            ADMIN
        ),
        (
            "Actualizar estado de un pago",
            actualizar_estado_pago_presentacion,
            ADMIN
        )
    ]

    mostrar_submenu(
        "GESTIÓN DE PAGOS",
        opciones,
        usuario_actual
    )


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

OPCIONES_PRINCIPALES = [
    ("Gestión de categorías", menu_categoria, TODOS),
    ("Gestión de marcas", abrir_menu_marcas, TODOS),
    ("Gestión de proveedores", menu_proveedores, TODOS),
    ("Gestión de productos", menu_productos, TODOS),
    ("Imágenes de productos", menu_imagenes_producto, TODOS),
    ("Valoraciones", menu_valoracion, TODOS),
    ("Mi carrito", menu_detalle_carrito, CLIENTE),
    ("Gestión de carritos", menu_carrito, ADMIN),
    ("Direcciones", menu_direccion, TODOS),
    ("Pedidos", menu_pedidos, TODOS),
    ("Pagos", menu_pagos, TODOS),
    ("Formas de pago", abrir_menu_formas_pago, TODOS),
    ("Gestión de stock", menu_movimiento_stock, ADMIN),
    ("Gestión de cupones", menu_cupones, ADMIN),
    ("Gestión de usuarios", menu_usuarios, ADMIN)
]


# ---------------------------------------------------------------------------
# Conexión a la base de datos
# ---------------------------------------------------------------------------

def inicializar_base_datos():
    if DB.is_closed():
        DB.connect()
        print("[Info] Conexión a la base de datos establecida.")


# ---------------------------------------------------------------------------
# Inicio de sesión
# ---------------------------------------------------------------------------

def mostrar_inicio_sesion():
    print("\n==================================")
    print("       TIENDA E-COMMERCE")
    print("==================================")
    print("1. Iniciar sesión")
    print("0. Salir")
    print("==================================")


def iniciar_sesion_obligatoria():
    global usuario_en_sesion

    while usuario_en_sesion is None:
        mostrar_inicio_sesion()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            usuario = procesar_login_presentacion()

            if usuario:
                usuario_en_sesion = usuario

        elif opcion == "0":
            return False

        else:
            print("\n[X] Opción no válida.")

    return True


# ---------------------------------------------------------------------------
# Menú principal en pantalla
# ---------------------------------------------------------------------------

def mostrar_menu_principal(opciones_visibles):
    print("\n==================================")
    print("       TIENDA E-COMMERCE")
    print("==================================")
    print(f"Usuario: {usuario_en_sesion.nombre}")
    print(f"Rol: {usuario_en_sesion.rol}")
    print("----------------------------------")

    numero = 1

    for opcion in opciones_visibles:
        print(f"{numero}. {opcion[0]}")
        numero += 1

    print("----------------------------------")
    print(f"{len(opciones_visibles) + 1}. Cerrar sesión")
    print(f"{len(opciones_visibles) + 2}. Salir")
    print("==================================")


# ---------------------------------------------------------------------------
# Cierre de sesión
# ---------------------------------------------------------------------------

def cerrar_sesion():
    global usuario_en_sesion

    usuario_en_sesion = None

    print("\n[✔] Sesión cerrada correctamente.")


# ---------------------------------------------------------------------------
# Ejecución del menú principal
# ---------------------------------------------------------------------------

def cargar_menu():
    global usuario_en_sesion

    inicializar_base_datos()

    try:
        while True:
            if usuario_en_sesion is None:
                if not iniciar_sesion_obligatoria():
                    break

            opciones_visibles = filtrar_opciones(
                OPCIONES_PRINCIPALES,
                es_administrador(usuario_en_sesion)
            )

            mostrar_menu_principal(opciones_visibles)

            opcion = input("Seleccione una opción: ").strip()

            if not opcion.isdigit():
                print("\n[X] Opción no válida.")
                continue

            numero = int(opcion)

            if 1 <= numero <= len(opciones_visibles):
                opciones_visibles[numero - 1][1](usuario_en_sesion)

            elif numero == len(opciones_visibles) + 1:
                cerrar_sesion()

            elif numero == len(opciones_visibles) + 2:
                print("\n¡Gracias por utilizar la tienda!")
                break

            else:
                print("\n[X] Opción no válida.")

    finally:
        usuario_en_sesion = None

        if not DB.is_closed():
            DB.close()


if __name__ == "__main__":
    cargar_menu()

