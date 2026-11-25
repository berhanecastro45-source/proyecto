
from prettytable import PrettyTable

from negocio.proveedor_negocio import (
    listar_proveedores_negocio,
    listar_proveedores_desactivados_negocio,
    crear_proveedor_negocio,
    actualizar_proveedor_negocio,
    eliminar_proveedor_negocio,
    reactivar_proveedor_negocio
)


def solicitar_id():
    while True:
        texto = input("\nIngrese el ID del proveedor: ").strip()

        if not texto.isdigit():
            print("[X] Debe ingresar un número entero válido.")
            continue

        id_proveedor = int(texto)

        if id_proveedor <= 0:
            print("[X] El ID debe ser positivo.")
            continue

        return id_proveedor


def solicitar_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje).strip().lower()

        if respuesta == "s":
            return True

        if respuesta == "n":
            return False

        print("[X] Responda únicamente S o N.")


def mostrar_tabla_proveedores(proveedores, titulo):
    if not proveedores:
        print("\n[X] No hay proveedores para mostrar.")
        return False

    tabla = PrettyTable()
    tabla.field_names = ["ID", "RUT", "Nombre", "Teléfono", "Email"]

    for proveedor in proveedores:
        tabla.add_row([
            proveedor.id_proveedor,
            proveedor.rut,
            proveedor.nombre,
            proveedor.telefono or "No registrado",
            proveedor.email
        ])

    print(f"\n--- {titulo} ---")
    print(tabla)

    return True


def obtener_proveedor_seleccionado(proveedores):
    while True:
        id_proveedor = solicitar_id()

        for proveedor in proveedores:
            if proveedor.id_proveedor == id_proveedor:
                return proveedor

        print("[X] El ID ingresado no pertenece al listado.")
        print("Ingrese un ID de la lista mostrada.")


def menu_proveedores(usuario_actual):
    rol = usuario_actual.rol if usuario_actual else None
    es_admin = isinstance(rol, str) and rol.strip().upper() == "ADMINISTRADOR"

    while True:
        print("\n--- MENÚ DE PROVEEDORES ---")
        print("1. Listar proveedores")

        if es_admin:
            print("2. Crear proveedor")
            print("3. Actualizar proveedor")
            print("4. Desactivar proveedor")
            print("5. Listar proveedores desactivados")
            print("6. Reactivar proveedor")
            print("7. Volver al menú principal")
        else:
            print("2. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            presentacion_listado_proveedores()

        elif opcion == "2" and es_admin:
            presentacion_crear_proveedor(rol)

        elif opcion == "3" and es_admin:
            presentacion_actualizar_proveedor(rol)

        elif opcion == "4" and es_admin:
            presentacion_eliminar_proveedor(rol)

        elif opcion == "5" and es_admin:
            presentacion_listado_proveedores_desactivados(rol)

        elif opcion == "6" and es_admin:
            presentacion_reactivar_proveedor(rol)

        elif (opcion == "7" and es_admin) or (opcion == "2" and not es_admin):
            break

        else:
            print("\n[X] Opción no válida o sin permisos.")


def presentacion_listado_proveedores():
    try:
        proveedores = listar_proveedores_negocio()

        mostrar_tabla_proveedores(
            proveedores,
            "LISTADO DE PROVEEDORES"
        )

    except (ValueError, PermissionError) as e:
        print(f"\n[X] Error: {e}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar los proveedores.")


def presentacion_listado_proveedores_desactivados(rol):
    try:
        proveedores = listar_proveedores_desactivados_negocio(rol)

        mostrar_tabla_proveedores(
            proveedores,
            "PROVEEDORES DESACTIVADOS"
        )

    except (ValueError, PermissionError) as e:
        print(f"\n[X] Error: {e}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar los proveedores desactivados.")


def presentacion_crear_proveedor(rol):
    print("\n--- REGISTRAR PROVEEDOR ---")

    rut = input("Ingrese el RUT del proveedor: ").strip()
    nombre = input("Ingrese el nombre del proveedor: ").strip()
    telefono = input("Ingrese el teléfono del proveedor (opcional): ").strip()
    email = input("Ingrese el correo electrónico: ").strip()

    if not telefono:
        telefono = None

    try:
        crear_proveedor_negocio(rut, nombre, telefono, email, rol)

        print("\n[✔] Proveedor registrado exitosamente.")

    except (ValueError, PermissionError) as e:
        print(f"\n[X] Error: {e}")

    except Exception:
        print("\n[X] Ocurrió un error al registrar el proveedor.")


def presentacion_actualizar_proveedor(rol):
    try:
        proveedores = listar_proveedores_negocio()

        if not mostrar_tabla_proveedores(
            proveedores,
            "PROVEEDORES DISPONIBLES PARA MODIFICAR"
        ):
            return

        proveedor = obtener_proveedor_seleccionado(proveedores)

        print(f"\n--- MODIFICAR PROVEEDOR: {proveedor.nombre} ---")
        print("Presione ENTER para conservar el dato actual.")
        print("Para eliminar el teléfono, escriba BORRAR.")

        rut = input(f"Nuevo RUT [{proveedor.rut}]: ").strip()

        if not rut:
            rut = proveedor.rut

        nombre = input(f"Nuevo nombre [{proveedor.nombre}]: ").strip()

        if not nombre:
            nombre = proveedor.nombre

        telefono_actual = proveedor.telefono or "No registrado"

        telefono = input(
            f"Nuevo teléfono [{telefono_actual}]: "
        ).strip()

        if not telefono:
            telefono = proveedor.telefono
        elif telefono.upper() == "BORRAR":
            telefono = None

        email = input(f"Nuevo correo [{proveedor.email}]: ").strip()

        if not email:
            email = proveedor.email

        if (
            rut == proveedor.rut
            and nombre == proveedor.nombre
            and telefono == proveedor.telefono
            and email == proveedor.email
        ):
            print("\nNo se realizaron cambios.")
            return

        actualizar_proveedor_negocio(
            proveedor.id_proveedor,
            rut,
            nombre,
            telefono,
            email,
            rol
        )

        print("\n[✔] Proveedor actualizado exitosamente.")

    except (ValueError, PermissionError) as e:
        print(f"\n[X] Error: {e}")

    except Exception:
        print("\n[X] Ocurrió un error al actualizar el proveedor.")


def presentacion_eliminar_proveedor(rol):
    try:
        proveedores = listar_proveedores_negocio()

        if not mostrar_tabla_proveedores(
            proveedores,
            "PROVEEDORES ACTIVOS PARA DESACTIVAR"
        ):
            return

        proveedor = obtener_proveedor_seleccionado(proveedores)

        confirmar = solicitar_confirmacion(
            f"\n¿Está seguro de desactivar el proveedor "
            f"'{proveedor.nombre}'? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        eliminar_proveedor_negocio(proveedor.id_proveedor, rol)

        print(
            f"\n[✔] Proveedor '{proveedor.nombre}' "
            f"desactivado exitosamente."
        )

    except (ValueError, PermissionError) as e:
        print(f"\n[X] Error: {e}")

    except Exception:
        print("\n[X] Ocurrió un error al desactivar el proveedor.")


def presentacion_reactivar_proveedor(rol):
    try:
        proveedores = listar_proveedores_desactivados_negocio(rol)

        if not mostrar_tabla_proveedores(
            proveedores,
            "PROVEEDORES DISPONIBLES PARA REACTIVAR"
        ):
            return

        proveedor = obtener_proveedor_seleccionado(proveedores)

        confirmar = solicitar_confirmacion(
            f"\n¿Desea reactivar el proveedor "
            f"'{proveedor.nombre}'? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        reactivar_proveedor_negocio(proveedor.id_proveedor, rol)

        print(
            f"\n[✔] Proveedor '{proveedor.nombre}' "
            f"reactivado exitosamente."
        )

    except (ValueError, PermissionError) as e:
        print(f"\n[X] Error: {e}")

    except Exception:
        print("\n[X] Ocurrió un error al reactivar el proveedor.")


