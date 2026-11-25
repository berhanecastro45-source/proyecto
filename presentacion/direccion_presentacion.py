from prettytable import PrettyTable

from negocio.direccion_negocio import (
    listar_direcciones_negocio,
    listar_todas_direcciones_negocio,
    buscar_direccion_negocio,
    crear_direccion_negocio,
    actualizar_direccion_negocio,
    eliminar_direccion_negocio
)


def solicitar_id():
    while True:
        try:
            id_direccion = int(
                input("Ingrese el ID de la dirección: ").strip()
            )

            if id_direccion <= 0:
                print("[X] El ID debe ser un número entero positivo.")
                continue

            return id_direccion

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


def solicitar_codigo_postal(mensaje, valor_actual=None, permitir_borrar=False):
    while True:
        codigo = input(mensaje).strip()

        if permitir_borrar and codigo.upper() == "BORRAR":
            return None

        if not codigo and valor_actual is not None:
            return valor_actual

        if not codigo:
            return None

        if len(codigo) > 20:
            print("[X] El código postal no puede superar los 20 caracteres.")
            continue

        return codigo


def solicitar_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje).strip().upper()

        if respuesta == "S":
            return True

        if respuesta == "N":
            return False

        print("[X] Responda únicamente S o N.")


def presentar_tabla_direcciones(direcciones, es_admin=False):
    if not direcciones:
        print("\nNo hay direcciones registradas.")
        return False

    tabla = PrettyTable()

    if es_admin:
        tabla.field_names = [
            "ID",
            "ID usuario",
            "Calle",
            "Ciudad",
            "Comuna",
            "Región",
            "Código postal"
        ]
    else:
        tabla.field_names = [
            "ID",
            "Calle",
            "Ciudad",
            "Comuna",
            "Región",
            "Código postal"
        ]

    for direccion in direcciones:
        fila = [
            direccion.id_direccion,
            direccion.calle,
            direccion.ciudad,
            direccion.comuna,
            direccion.region,
            direccion.codigo_postal or "No registrado"
        ]

        if es_admin:
            fila.insert(1, direccion.id_usuario)

        tabla.add_row(fila)

    print(tabla)
    return True


def obtener_direccion_seleccionada(direcciones):
    if not presentar_tabla_direcciones(direcciones):
        return None

    while True:
        id_direccion = solicitar_id()

        for direccion in direcciones:
            if direccion.id_direccion == id_direccion:
                return direccion

        print("[X] El ID no pertenece al listado mostrado.")


def presentar_listar_direcciones(usuario_actual):
    try:
        direcciones = listar_direcciones_negocio(usuario_actual)

        presentar_tabla_direcciones(direcciones)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar tus direcciones.")


def presentar_listar_todas_direcciones(usuario_actual):
    try:
        direcciones = listar_todas_direcciones_negocio(usuario_actual)

        presentar_tabla_direcciones(direcciones, True)

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al consultar las direcciones.")


def presentar_buscar_direccion(usuario_actual):
    try:
        direcciones = listar_direcciones_negocio(usuario_actual)

        direccion_seleccionada = obtener_direccion_seleccionada(
            direcciones
        )

        if direccion_seleccionada is None:
            return

        direccion = buscar_direccion_negocio(
            direccion_seleccionada.id_direccion,
            usuario_actual
        )

        print("\n========== INFORMACIÓN DE LA DIRECCIÓN ==========")

        presentar_tabla_direcciones([direccion])

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al buscar la dirección.")


def presentar_crear_direccion(usuario_actual):
    print("\n========== REGISTRAR DIRECCIÓN ==========")

    try:
        calle = solicitar_texto(
            "Ingrese calle y número: ",
            "La calle",
            150
        )

        ciudad = solicitar_texto(
            "Ingrese ciudad: ",
            "La ciudad",
            100
        )

        comuna = solicitar_texto(
            "Ingrese comuna: ",
            "La comuna",
            100
        )

        region = solicitar_texto(
            "Ingrese región: ",
            "La región",
            100
        )

        codigo_postal = solicitar_codigo_postal(
            "Ingrese código postal (opcional): "
        )

        crear_direccion_negocio(
            calle,
            ciudad,
            comuna,
            region,
            codigo_postal,
            usuario_actual
        )

        print("\n[✔] Dirección registrada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al registrar la dirección.")


def solicitar_datos_actualizados(direccion):
    print("\n========== MODIFICAR DIRECCIÓN ==========")
    print("Presione ENTER para conservar el dato actual.")
    print("Para eliminar el código postal, escriba BORRAR.")

    calle = solicitar_texto(
        f"Nueva calle y número [{direccion.calle}]: ",
        "La calle",
        150,
        direccion.calle
    )

    ciudad = solicitar_texto(
        f"Nueva ciudad [{direccion.ciudad}]: ",
        "La ciudad",
        100,
        direccion.ciudad
    )

    comuna = solicitar_texto(
        f"Nueva comuna [{direccion.comuna}]: ",
        "La comuna",
        100,
        direccion.comuna
    )

    region = solicitar_texto(
        f"Nueva región [{direccion.region}]: ",
        "La región",
        100,
        direccion.region
    )

    codigo_actual = direccion.codigo_postal or "No registrado"

    codigo_postal = solicitar_codigo_postal(
        f"Nuevo código postal [{codigo_actual}]: ",
        direccion.codigo_postal,
        True
    )

    return (
        calle,
        ciudad,
        comuna,
        region,
        codigo_postal
    )


def presentar_actualizar_direccion(usuario_actual):
    print("\n========== ACTUALIZAR DIRECCIÓN ==========")

    try:
        direcciones = listar_direcciones_negocio(usuario_actual)

        direccion = obtener_direccion_seleccionada(direcciones)

        if direccion is None:
            return

        datos = solicitar_datos_actualizados(direccion)

        if (
            datos[0] == direccion.calle
            and datos[1] == direccion.ciudad
            and datos[2] == direccion.comuna
            and datos[3] == direccion.region
            and datos[4] == direccion.codigo_postal
        ):
            print("\nNo se realizaron cambios.")
            return

        actualizar_direccion_negocio(
            direccion.id_direccion,
            datos[0],
            datos[1],
            datos[2],
            datos[3],
            datos[4],
            usuario_actual
        )

        print("\n[✔] Dirección actualizada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al actualizar la dirección.")


def presentar_eliminar_direccion(usuario_actual):
    print("\n========== DESACTIVAR DIRECCIÓN ==========")

    try:
        direcciones = listar_direcciones_negocio(usuario_actual)

        direccion = obtener_direccion_seleccionada(direcciones)

        if direccion is None:
            return

        confirmar = solicitar_confirmacion(
            "\n¿Está seguro de desactivar esta dirección? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        eliminar_direccion_negocio(
            direccion.id_direccion,
            usuario_actual
        )

        print("\n[✔] Dirección desactivada correctamente.")

    except (ValueError, PermissionError) as error:
        print(f"\n[X] Error: {error}")

    except Exception:
        print("\n[X] Ocurrió un error al desactivar la dirección.")


def menu_direccion(usuario_actual):
    rol = getattr(usuario_actual, "rol", "")
    es_admin = (
        isinstance(rol, str)
        and rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n========== GESTIÓN DE DIRECCIONES ==========")
        print("1. Listar mis direcciones")
        print("2. Buscar una dirección")
        print("3. Registrar una dirección")
        print("4. Actualizar una dirección")
        print("5. Desactivar una dirección")

        if es_admin:
            print("6. Listar todas las direcciones")

        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            presentar_listar_direcciones(usuario_actual)

        elif opcion == "2":
            presentar_buscar_direccion(usuario_actual)

        elif opcion == "3":
            presentar_crear_direccion(usuario_actual)

        elif opcion == "4":
            presentar_actualizar_direccion(usuario_actual)

        elif opcion == "5":
            presentar_eliminar_direccion(usuario_actual)

        elif opcion == "6" and es_admin:
            presentar_listar_todas_direcciones(usuario_actual)

        elif opcion == "0":
            break

        else:
            print("\n[X] Opción inválida o sin permisos.")