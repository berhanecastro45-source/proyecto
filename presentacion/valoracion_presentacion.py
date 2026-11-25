
from prettytable import PrettyTable

from negocio.valoracion_negocio import (
    listar_valoraciones_negocio,
    listar_valoraciones_producto_negocio,
    listar_valoraciones_usuario_negocio,
    listar_valoraciones_desactivadas_negocio,
    buscar_valoracion_negocio,
    crear_valoracion_negocio,
    actualizar_valoracion_negocio,
    eliminar_valoracion_negocio,
    reactivar_valoracion_negocio
)


def solicitar_id(mensaje="Ingrese el ID de la valoración: "):
    while True:
        try:
            id_registro = int(input(mensaje).strip())

            if id_registro <= 0:
                print("El ID debe ser positivo.")
                continue

            return id_registro

        except ValueError:
            print("Debe ingresar un número entero válido.")


def solicitar_puntuacion():
    while True:
        try:
            puntuacion = int(
                input("Ingrese una puntuación de 1 a 5: ").strip()
            )

            if puntuacion < 1 or puntuacion > 5:
                print("La puntuación debe estar entre 1 y 5.")
                continue

            return puntuacion

        except ValueError:
            print("Debe ingresar un número entero válido.")


def solicitar_confirmacion(mensaje):
    while True:
        confirmacion = input(
            f"{mensaje} (S/N): "
        ).strip().upper()

        if confirmacion == "S":
            return True

        if confirmacion == "N":
            return False

        print("Ingrese S para confirmar o N para cancelar.")


def presentar_tabla_valoraciones(
    valoraciones,
    es_admin=False,
    mostrar_estado=False
):
    if not valoraciones:
        print("No hay valoraciones registradas.")
        return False

    tabla = PrettyTable()

    tabla.field_names = [
        "ID",
        "ID usuario",
        "ID producto",
        "Puntuación",
        "Comentario",
        "Fecha"
    ]

    if mostrar_estado:
        tabla.field_names.append("Estado")

    for valoracion in valoraciones:
        fila = [
            valoracion.id_valoracion,
            valoracion.id_usuario,
            valoracion.id_producto,
            valoracion.puntuacion,
            valoracion.comentario or "Sin comentario",
            valoracion.fecha_valoracion
        ]

        if mostrar_estado:
            if valoracion.activo == 1:
                fila.append("Activa")
            else:
                fila.append("Desactivada")

        if not es_admin:
            fila.pop(1)

        tabla.add_row(fila)

    print(tabla)
    return True


def presentacion_listar_valoraciones(usuario_actual):
    try:
        valoraciones = listar_valoraciones_negocio(usuario_actual)

        presentar_tabla_valoraciones(
            valoraciones,
            es_admin=True
        )

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print("Ocurrió un error al consultar las valoraciones.")


def presentacion_listar_valoraciones_producto():
    try:
        id_producto = solicitar_id(
            "Ingrese el ID del producto: "
        )

        valoraciones = listar_valoraciones_producto_negocio(
            id_producto
        )

        presentar_tabla_valoraciones(valoraciones)

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print(
            "Ocurrió un error al consultar las valoraciones del producto."
        )


def presentacion_listar_valoraciones_usuario(usuario_actual):
    try:
        valoraciones = listar_valoraciones_usuario_negocio(
            usuario_actual
        )

        presentar_tabla_valoraciones(valoraciones)

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print("Ocurrió un error al consultar tus valoraciones.")


def presentacion_listar_valoraciones_desactivadas(usuario_actual):
    try:
        valoraciones = listar_valoraciones_desactivadas_negocio(
            usuario_actual
        )

        es_admin = (
            usuario_actual.rol.strip().upper() == "ADMINISTRADOR"
        )

        presentar_tabla_valoraciones(
            valoraciones,
            es_admin,
            mostrar_estado=True
        )

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print(
            "Ocurrió un error al consultar las valoraciones desactivadas."
        )


def presentacion_buscar_valoracion(usuario_actual):
    try:
        id_valoracion = solicitar_id()

        valoracion = buscar_valoracion_negocio(
            id_valoracion,
            usuario_actual
        )

        presentar_tabla_valoraciones([valoracion])

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print("Ocurrió un error al buscar la valoración.")


def presentacion_crear_valoracion(usuario_actual):
    try:
        id_producto = solicitar_id(
            "Ingrese el ID del producto: "
        )

        puntuacion = solicitar_puntuacion()

        comentario = input(
            "Ingrese un comentario (opcional): "
        ).strip()

        crear_valoracion_negocio(
            id_producto,
            puntuacion,
            comentario or None,
            usuario_actual
        )

        print("Valoración registrada exitosamente.")

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print("Ocurrió un error al registrar la valoración.")


def presentacion_actualizar_valoracion(usuario_actual):
    try:
        valoraciones = listar_valoraciones_usuario_negocio(
            usuario_actual
        )

        if not presentar_tabla_valoraciones(valoraciones):
            return

        id_valoracion = solicitar_id()

        valoracion = buscar_valoracion_negocio(
            id_valoracion,
            usuario_actual
        )

        print("\nIngrese los nuevos datos.")
        print("Presione ENTER para conservar el comentario actual.")
        print("Escriba BORRAR para eliminar el comentario.")

        puntuacion = solicitar_puntuacion()

        comentario = input(
            "Nuevo comentario: "
        ).strip()

        if comentario == "":
            comentario = valoracion.comentario

        elif comentario.upper() == "BORRAR":
            comentario = None

        actualizar_valoracion_negocio(
            id_valoracion,
            puntuacion,
            comentario,
            usuario_actual
        )

        print("Valoración actualizada exitosamente.")

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print("Ocurrió un error al actualizar la valoración.")


def presentacion_eliminar_valoracion(usuario_actual):
    try:
        valoraciones = listar_valoraciones_usuario_negocio(
            usuario_actual
        )

        if not presentar_tabla_valoraciones(valoraciones):
            return

        id_valoracion = solicitar_id()

        if not solicitar_confirmacion(
            "¿Está seguro de desactivar esta valoración?"
        ):
            print("Operación cancelada.")
            return

        eliminar_valoracion_negocio(
            id_valoracion,
            usuario_actual
        )

        print("Valoración desactivada exitosamente.")

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print("Ocurrió un error al desactivar la valoración.")


def presentacion_reactivar_valoracion(usuario_actual):
    try:
        valoraciones = listar_valoraciones_desactivadas_negocio(
            usuario_actual
        )

        es_admin = (
            usuario_actual.rol.strip().upper() == "ADMINISTRADOR"
        )

        if not presentar_tabla_valoraciones(
            valoraciones,
            es_admin,
            mostrar_estado=True
        ):
            return

        id_valoracion = solicitar_id()

        if not solicitar_confirmacion(
            "¿Desea reactivar esta valoración?"
        ):
            print("Operación cancelada.")
            return

        reactivar_valoracion_negocio(
            id_valoracion,
            usuario_actual
        )

        print("Valoración reactivada exitosamente.")

    except (ValueError, PermissionError) as error:
        print(f"Error: {error}")

    except Exception:
        print("Ocurrió un error al reactivar la valoración.")


def menu_valoracion(usuario_actual):
    es_admin = (
        usuario_actual.rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n========== GESTIÓN DE VALORACIONES ==========")
        print("1. Ver valoraciones de un producto")
        print("2. Ver mis valoraciones")
        print("3. Registrar valoración")
        print("4. Buscar mi valoración")
        print("5. Actualizar valoración")
        print("6. Desactivar valoración")
        print("7. Ver mis valoraciones desactivadas")
        print("8. Reactivar valoración")

        if es_admin:
            print("9. Listar todas las valoraciones")
            print("10. Listar todas las valoraciones desactivadas")

        print("0. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            presentacion_listar_valoraciones_producto()

        elif opcion == "2":
            presentacion_listar_valoraciones_usuario(
                usuario_actual
            )

        elif opcion == "3":
            presentacion_crear_valoracion(usuario_actual)

        elif opcion == "4":
            presentacion_buscar_valoracion(usuario_actual)

        elif opcion == "5":
            presentacion_actualizar_valoracion(usuario_actual)

        elif opcion == "6":
            presentacion_eliminar_valoracion(usuario_actual)

        elif opcion == "7":
            presentacion_listar_valoraciones_desactivadas(
                usuario_actual
            )

        elif opcion == "8":
            presentacion_reactivar_valoracion(usuario_actual)

        elif opcion == "9" and es_admin:
            presentacion_listar_valoraciones(usuario_actual)

        elif opcion == "10" and es_admin:
            presentacion_listar_valoraciones_desactivadas(
                usuario_actual
            )

        elif opcion == "0":
            break

        else:
            print("Opción inválida o sin permisos.")

