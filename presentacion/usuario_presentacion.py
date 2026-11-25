
import re
import maskpass
from datetime import datetime, date

from negocio.usuario_negocio import (
    registrar_usuario_negocio,
    login_usuario_negocio,
    listar_usuarios_negocio,
    obtener_usuario_para_actualizar_negocio,
    actualizar_usuario_negocio,
    desactivar_usuario_negocio,
    validar_rut,
    validar_rut_disponible,
    listar_usuarios_inactivos_negocio,
    activar_usuario_negocio
)


def solicitar_id_usuario():
    while True:
        id_usuario = input("Ingrese el ID del usuario: ").strip()

        if id_usuario.isdigit() and int(id_usuario) > 0:
            return int(id_usuario)

        print("Ingrese un ID válido y positivo.")


def solicitar_confirmacion(mensaje):
    while True:
        respuesta = input(mensaje).strip().upper()

        if respuesta == "S":
            return True

        if respuesta == "N":
            return False

        print("Responda únicamente S o N.")


def solicitar_texto_valido(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto and re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", texto):
            return texto.title()

        print("Ingrese un texto válido.")


def solicitar_apellido_materno():
    while True:
        texto = input("Apellido materno (opcional): ").strip()

        if not texto:
            return None

        if re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+", texto):
            return texto.title()

        print("Ingrese un apellido válido.")


def solicitar_rut():
    while True:
        rut = input("RUT (sin puntos ni guion): ").strip()
        rut = rut.replace(".", "").replace("-", "").upper()

        if re.fullmatch(r"\d{7,8}[0-9K]", rut):
            if not validar_rut(rut):
                print("El RUT ingresado no es válido. Revise el dígito verificador.")
                continue

            if not validar_rut_disponible(rut):
                print("Este RUT ya está registrado.")
                continue

            return rut

        print("Ingrese un RUT válido.")


def solicitar_fecha_nacimiento():
    while True:
        try:
            texto = input("Fecha de nacimiento (DD-MM-AAAA): ").strip()
            fecha = datetime.strptime(texto, "%d-%m-%Y").date()

            hoy = date.today()
            edad = hoy.year - fecha.year

            if (hoy.month, hoy.day) < (fecha.month, fecha.day):
                edad -= 1

            if edad < 18 or edad > 120:
                print("Debe tener entre 18 y 120 años.")
                continue

            return fecha

        except ValueError:
            print("Ingrese una fecha válida usando el formato DD-MM-AAAA.")


def solicitar_email():
    while True:
        email = input("Correo electrónico: ").strip().lower()

        if re.fullmatch(r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}", email):
            return email

        print("Ingrese un correo electrónico válido.")


def solicitar_telefono():
    while True:
        telefono = input("Teléfono: ").strip()

        if telefono.isdigit() and 7 <= len(telefono) <= 15:
            return telefono

        print("Ingrese un teléfono válido.")


def solicitar_password():
    while True:
        password = maskpass.askpass(prompt="Contraseña: ")

        if len(password) < 8:
            print("Debe tener al menos 8 caracteres.")
        elif not re.search(r"[A-Z]", password):
            print("Debe contener una mayúscula.")
        elif not re.search(r"[a-z]", password):
            print("Debe contener una minúscula.")
        elif not re.search(r"\d", password):
            print("Debe contener un número.")
        elif not re.search(r"[@$!%*?&.#_-]", password):
            print("Debe contener un carácter especial.")
        else:
            return password


def solicitar_campo_obligatorio(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto:
            return texto

        print("Este campo es obligatorio.")


def solicitar_direccion():
    print("\nDatos de dirección")

    return {
        "calle": solicitar_campo_obligatorio("Calle y número: "),
        "ciudad": solicitar_texto_valido("Ciudad: "),
        "comuna": solicitar_texto_valido("Comuna: "),
        "region": solicitar_texto_valido("Región: "),
        "codigo_postal": input("Código postal (opcional): ").strip() or None
    }


def pedir_datos_usuario():
    print("\nRegistro de usuario")

    datos = {
        "rut": solicitar_rut(),
        "nombre": solicitar_texto_valido("Nombre: "),
        "apellido_paterno": solicitar_texto_valido("Apellido paterno: "),
        "apellido_materno": solicitar_apellido_materno(),
        "email": solicitar_email(),
        "telefono": solicitar_telefono(),
        "fecha_nacimiento": solicitar_fecha_nacimiento(),
        "password": solicitar_password()
    }

    direccion = solicitar_direccion()

    return datos, direccion


def mostrar_error(error):
    print("\nError:", error)


def mostrar_error_general(mensaje):
    print("\n", mensaje)


def mostrar_tabla_usuarios(usuarios, titulo):
    print(f"\n--- {titulo} ---")

    if not usuarios:
        print("No hay usuarios para mostrar.")
        return False

    for usuario in usuarios:
        print(
            f"ID: {usuario.id_usuario} | "
            f"RUT: {usuario.rut} | "
            f"Nombre: {usuario.nombre} {usuario.apellido_paterno} | "
            f"Email: {usuario.email} | "
            f"Rol: {usuario.rol}"
        )

    return True


def obtener_usuario_seleccionado(usuarios):
    while True:
        id_usuario = solicitar_id_usuario()

        for usuario in usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario

        print("El ID ingresado no pertenece al listado.")
        print("Ingrese un ID de la lista mostrada.")


def presentacion_registrar_usuario():
    try:
        datos, direccion = pedir_datos_usuario()

        registrar_usuario_negocio(datos, direccion)

        print("\nUsuario registrado correctamente.")

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general("Ocurrió un error al registrar el usuario.")


def presentacion_listar_usuarios(usuario_actual):
    try:
        usuarios = listar_usuarios_negocio(usuario_actual)

        mostrar_tabla_usuarios(usuarios, "LISTADO DE USUARIOS")

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general("Ocurrió un error al consultar los usuarios.")


def presentacion_actualizar_usuario(usuario_actual):
    try:
        usuarios = listar_usuarios_negocio(usuario_actual)

        if not mostrar_tabla_usuarios(
            usuarios,
            "USUARIOS DISPONIBLES PARA MODIFICAR"
        ):
            return

        usuario = obtener_usuario_seleccionado(usuarios)

        usuario = obtener_usuario_para_actualizar_negocio(
            usuario.id_usuario,
            usuario_actual
        )

        print("\nPresione ENTER para conservar el dato actual.")
        print("Escriba BORRAR para eliminar el apellido materno o teléfono.")

        rut = input(f"RUT actual ({usuario.rut}): ").strip()
        nombre = input(f"Nombre actual ({usuario.nombre}): ").strip()

        apellido_paterno = input(
            f"Apellido paterno actual ({usuario.apellido_paterno}): "
        ).strip()

        apellido_materno = input(
            f"Apellido materno actual ({usuario.apellido_materno or 'Sin dato'}): "
        ).strip()

        email = input(f"Email actual ({usuario.email}): ").strip().lower()

        telefono = input(
            f"Teléfono actual ({usuario.telefono or 'Sin dato'}): "
        ).strip()

        if apellido_materno.upper() == "BORRAR":
            apellido_materno = None
        elif not apellido_materno:
            apellido_materno = usuario.apellido_materno
        else:
            apellido_materno = apellido_materno.title()

        if telefono.upper() == "BORRAR":
            telefono = None
        elif not telefono:
            telefono = usuario.telefono

        datos = {
            "rut": rut or usuario.rut,
            "nombre": nombre.title() if nombre else usuario.nombre,
            "apellido_paterno": (
                apellido_paterno.title()
                if apellido_paterno
                else usuario.apellido_paterno
            ),
            "apellido_materno": apellido_materno,
            "email": email or usuario.email,
            "telefono": telefono
        }

        if (
            datos["rut"] == usuario.rut
            and datos["nombre"] == usuario.nombre
            and datos["apellido_paterno"] == usuario.apellido_paterno
            and datos["apellido_materno"] == usuario.apellido_materno
            and datos["email"] == usuario.email
            and datos["telefono"] == usuario.telefono
        ):
            print("\nNo se realizaron cambios.")
            return

        actualizar_usuario_negocio(
            usuario.id_usuario,
            datos,
            usuario_actual
        )

        print("\nUsuario actualizado correctamente.")

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general("Ocurrió un error al actualizar el usuario.")


def presentacion_desactivar_usuario(usuario_actual):
    try:
        usuarios = listar_usuarios_negocio(usuario_actual)

        if not mostrar_tabla_usuarios(usuarios, "USUARIOS ACTIVOS"):
            return

        usuario = obtener_usuario_seleccionado(usuarios)

        confirmar = solicitar_confirmacion(
            f"\n¿Está seguro de desactivar al usuario "
            f"'{usuario.nombre} {usuario.apellido_paterno}'? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        desactivar_usuario_negocio(usuario.id_usuario, usuario_actual)

        print("\nUsuario desactivado correctamente.")

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general("Ocurrió un error al desactivar el usuario.")


def presentacion_activar_usuario(usuario_actual):
    try:
        usuarios = listar_usuarios_inactivos_negocio(usuario_actual)

        if not mostrar_tabla_usuarios(usuarios, "USUARIOS DESACTIVADOS"):
            return

        usuario = obtener_usuario_seleccionado(usuarios)

        confirmar = solicitar_confirmacion(
            f"\n¿Está seguro de activar al usuario "
            f"'{usuario.nombre} {usuario.apellido_paterno}'? (S/N): "
        )

        if not confirmar:
            print("\nOperación cancelada.")
            return

        activar_usuario_negocio(usuario.id_usuario, usuario_actual)

        print("\nUsuario activado correctamente.")

    except (ValueError, PermissionError) as error:
        mostrar_error(error)

    except Exception:
        mostrar_error_general("Ocurrió un error al activar el usuario.")


def menu_usuarios(usuario_actual):
    while True:
        print("\n--- ADMINISTRACIÓN DE USUARIOS ---")
        print("1. Registrar usuario")
        print("2. Listar usuarios")
        print("3. Modificar usuario")
        print("4. Desactivar usuario")
        print("5. Activar usuario")
        print("6. Volver")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            presentacion_registrar_usuario()

        elif opcion == "2":
            presentacion_listar_usuarios(usuario_actual)

        elif opcion == "3":
            presentacion_actualizar_usuario(usuario_actual)

        elif opcion == "4":
            presentacion_desactivar_usuario(usuario_actual)

        elif opcion == "5":
            presentacion_activar_usuario(usuario_actual)

        elif opcion == "6":
            break

        else:
            print("Opción no válida.")


def procesar_login():
    print("\n--- INICIO DE SESIÓN ---")

    email = input("Correo electrónico: ").strip().lower()
    password = maskpass.askpass(prompt="Contraseña: ")

    try:
        usuario = login_usuario_negocio(email, password)

        if usuario is None:
            print("\nCorreo o contraseña incorrectos.")
            return None

        print(f"\nBienvenido/a, {usuario.nombre}.")

        return usuario

    except Exception:
        mostrar_error_general("Ocurrió un error al iniciar sesión.")
        return None

