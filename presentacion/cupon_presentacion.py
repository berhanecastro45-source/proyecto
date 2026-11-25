
from prettytable import PrettyTable

from negocio.cupon_negocio import (
    listar_cupones_negocio,
    listar_cupones_desactivados_negocio,
    buscar_cupon_negocio,
    crear_cupon_negocio,
    actualizar_cupon_negocio,
    eliminar_cupon_negocio,
    reactivar_cupon_negocio,
    validar_codigo,
    validar_descuento,
    validar_fecha,
    validar_fechas
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


def solicitar_confirmacion(mensaje):
    while True:
        confirmacion = input(mensaje).strip().lower()

        if confirmacion == "s":
            return True

        if confirmacion == "n":
            return False

        print("[X] Responda únicamente S o N.")


def presentar_tabla_cupones(cupones):
    if not cupones:
        print("\nNo hay cupones registrados.")
        return False

    tabla = PrettyTable()

    tabla.field_names = [
        "ID",
        "Código",
        "Descuento (%)",
        "Fecha inicio",
        "Fecha término"
    ]

    for cupon in cupones:
        tabla.add_row([
            cupon.id_cupon,
            cupon.codigo,
            cupon.descuento,
            cupon.fecha_inicio,
            cupon.fecha_fin
        ])

    print(tabla)
    return True


def obtener_cupon_seleccionado(cupones):
    while True:
        id_cupon = solicitar_entero(
            "Ingrese el ID del cupón: "
        )

        for cupon in cupones:
            if cupon.id_cupon == id_cupon:
                return cupon

        print("[X] El ID ingresado no pertenece a la lista.")


def solicitar_codigo(mensaje, codigo_actual=None):
    while True:
        codigo = input(mensaje).strip()

        if codigo == "" and codigo_actual is not None:
            return codigo_actual

        try:
            return validar_codigo(codigo)

        except ValueError as error:
            print(f"[X] {error}")


def solicitar_descuento(mensaje, descuento_actual=None):
    while True:
        descuento = input(mensaje).strip()

        if descuento == "" and descuento_actual is not None:
            return descuento_actual

        try:
            return validar_descuento(descuento)

        except ValueError as error:
            print(f"[X] {error}")


def solicitar_fecha(mensaje, nombre, fecha_actual=None):
    while True:
        fecha = input(mensaje).strip()

        if fecha == "" and fecha_actual is not None:
            return fecha_actual

        try:
            return validar_fecha(fecha, nombre)

        except ValueError as error:
            print(f"[X] {error}")


def solicitar_fecha_termino(fecha_inicio, fecha_actual=None):
    while True:
        fecha_fin = solicitar_fecha(
            "Ingrese la fecha de término (AAAA-MM-DD): ",
            "fecha de término",
            fecha_actual
        )

        try:
            validar_fechas(fecha_inicio, fecha_fin)
            return fecha_fin

        except ValueError as error:
            print(f"[X] {error}")


def presentar_listado_cupones(usuario_actual):
    cupones = listar_cupones_negocio(usuario_actual)
    presentar_tabla_cupones(cupones)


def presentacion_listar_cupones(usuario_actual):
    try:
        presentar_listado_cupones(usuario_actual)

    except (PermissionError, ValueError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar los cupones.")


def presentacion_buscar_cupon(usuario_actual):
    try:
        cupones = listar_cupones_negocio(usuario_actual)

        if not presentar_tabla_cupones(cupones):
            return

        cupon_seleccionado = obtener_cupon_seleccionado(cupones)

        cupon = buscar_cupon_negocio(
            cupon_seleccionado.id_cupon,
            usuario_actual
        )

        presentar_tabla_cupones([cupon])

    except (PermissionError, ValueError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al buscar el cupón.")


def presentacion_crear_cupon(usuario_actual):
    try:
        print("\n--- REGISTRAR CUPÓN ---")

        codigo = solicitar_codigo(
            "Ingrese el código del cupón: "
        )

        descuento = solicitar_descuento(
            "Ingrese el porcentaje de descuento: "
        )

        fecha_inicio = solicitar_fecha(
            "Ingrese la fecha de inicio (AAAA-MM-DD): ",
            "fecha de inicio"
        )

        fecha_fin = solicitar_fecha_termino(fecha_inicio)

        cupon = crear_cupon_negocio(
            codigo,
            descuento,
            fecha_inicio,
            fecha_fin,
            usuario_actual
        )

        print(
            f"\n[✔] Cupón '{cupon.codigo}' registrado correctamente."
        )

    except (PermissionError, ValueError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al registrar el cupón.")


def presentacion_actualizar_cupon(usuario_actual):
    try:
        cupones = listar_cupones_negocio(usuario_actual)

        if not presentar_tabla_cupones(cupones):
            return

        cupon = obtener_cupon_seleccionado(cupones)

        print("\n--- ACTUALIZAR CUPÓN ---")
        print("Presione ENTER para conservar el dato actual.\n")

        codigo = solicitar_codigo(
            f"Código actual ({cupon.codigo}): ",
            cupon.codigo
        )

        descuento = solicitar_descuento(
            f"Descuento actual ({cupon.descuento}): ",
            cupon.descuento
        )

        fecha_inicio = solicitar_fecha(
            f"Fecha de inicio actual ({cupon.fecha_inicio}): ",
            "fecha de inicio",
            cupon.fecha_inicio
        )

        fecha_fin = solicitar_fecha_termino(
            fecha_inicio,
            cupon.fecha_fin
        )

        if (
            codigo == cupon.codigo
            and str(descuento) == str(cupon.descuento)
            and fecha_inicio == cupon.fecha_inicio
            and fecha_fin == cupon.fecha_fin
        ):
            print("\nNo se realizaron cambios en el cupón.")
            return

        cupon_actualizado = actualizar_cupon_negocio(
            cupon.id_cupon,
            codigo,
            descuento,
            fecha_inicio,
            fecha_fin,
            usuario_actual
        )

        print(
            f"\n[✔] Cupón '{cupon_actualizado.codigo}' "
            "actualizado correctamente."
        )

    except (PermissionError, ValueError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al actualizar el cupón.")


def presentacion_eliminar_cupon(usuario_actual):
    try:
        cupones = listar_cupones_negocio(usuario_actual)

        if not presentar_tabla_cupones(cupones):
            return

        cupon = obtener_cupon_seleccionado(cupones)

        confirmar = solicitar_confirmacion(
            f"\n¿Está seguro de desactivar el cupón "
            f"'{cupon.codigo}'? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        eliminar_cupon_negocio(
            cupon.id_cupon,
            usuario_actual
        )

        print("\n[✔] Cupón desactivado correctamente.")

    except (PermissionError, ValueError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al desactivar el cupón.")


def presentacion_listar_cupones_desactivados(usuario_actual):
    try:
        cupones = listar_cupones_desactivados_negocio(
            usuario_actual
        )

        if not presentar_tabla_cupones(cupones):
            print("\nNo hay cupones desactivados.")
            return

        print("\n========== CUPONES DESACTIVADOS ==========")

    except (PermissionError, ValueError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar los cupones desactivados.")


def presentacion_reactivar_cupon(usuario_actual):
    try:
        cupones = listar_cupones_desactivados_negocio(
            usuario_actual
        )

        if not presentar_tabla_cupones(cupones):
            print("\nNo hay cupones disponibles para reactivar.")
            return

        print("\n========== REACTIVAR CUPÓN ==========")

        cupon = obtener_cupon_seleccionado(cupones)

        confirmar = solicitar_confirmacion(
            f"\n¿Está seguro de reactivar el cupón "
            f"'{cupon.codigo}'? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        reactivar_cupon_negocio(
            cupon.id_cupon,
            usuario_actual
        )

        print(
            f"\n[✔] Cupón '{cupon.codigo}' reactivado correctamente."
        )

    except (PermissionError, ValueError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al reactivar el cupón.")


def menu_cupones(usuario_actual):
    while True:
        print("\n========== GESTIÓN DE CUPONES ==========")
        print("1. Listar cupones activos")
        print("2. Buscar cupón por ID")
        print("3. Registrar cupón")
        print("4. Actualizar cupón")
        print("5. Desactivar cupón")
        print("6. Listar cupones desactivados")
        print("7. Reactivar cupón")
        print("0. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            presentacion_listar_cupones(usuario_actual)

        elif opcion == "2":
            presentacion_buscar_cupon(usuario_actual)

        elif opcion == "3":
            presentacion_crear_cupon(usuario_actual)

        elif opcion == "4":
            presentacion_actualizar_cupon(usuario_actual)

        elif opcion == "5":
            presentacion_eliminar_cupon(usuario_actual)

        elif opcion == "6":
            presentacion_listar_cupones_desactivados(usuario_actual)

        elif opcion == "7":
            presentacion_reactivar_cupon(usuario_actual)

        elif opcion == "0":
            break

        else:
            print("\n[X] Opción no válida. Intente nuevamente.")
