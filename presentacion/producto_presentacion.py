
from decimal import Decimal, InvalidOperation
from prettytable import PrettyTable

from negocio.producto_negocio import (
    listar_productos_negocio,
    listar_productos_desactivados_negocio,
    buscar_producto_negocio,
    crear_producto_negocio,
    actualizar_producto_negocio,
    eliminar_producto_negocio,
    reactivar_producto_negocio
)

from negocio.categoria_negocio import listar_categorias_negocio
from negocio.marca_negocio import listar_marcas_negocio
from negocio.proveedor_negocio import listar_proveedores_negocio


def solicitar_entero(mensaje, minimo=0):
    while True:
        try:
            valor = int(input(mensaje).strip())

            if valor < minimo:
                print(f"[X] El valor debe ser igual o mayor que {minimo}.")
                continue

            return valor

        except ValueError:
            print("[X] Debe ingresar un número entero válido.")


def solicitar_precio(mensaje):
    while True:
        texto = input(mensaje).strip()

        try:
            precio = Decimal(texto)

            if not precio.is_finite() or precio <= 0:
                print("[X] El precio debe ser un número mayor que cero.")
                continue

            if precio.as_tuple().exponent < -2:
                print("[X] El precio admite como máximo dos decimales.")
                continue

            if precio >= Decimal("100000000"):
                print("[X] El precio supera el máximo permitido.")
                continue

            return precio

        except InvalidOperation:
            print("[X] Ingrese un precio válido.")


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


def mostrar_tabla_productos(productos, titulo):
    if not productos:
        print("\n[X] No hay productos para mostrar.")
        return False

    tabla = PrettyTable()
    tabla.field_names = [
        "ID", "Nombre", "Precio", "Stock",
        "Stock mínimo", "Categoría", "Marca", "Proveedor"
    ]

    for producto in productos:
        tabla.add_row([
            producto.id_producto,
            producto.nombre,
            producto.precio,
            producto.stock,
            producto.stock_minimo,
            producto.nombre_categoria,
            producto.nombre_marca,
            producto.nombre_proveedor
        ])

    print(f"\n--- {titulo} ---")
    print(tabla)

    return True


def obtener_producto_seleccionado(productos):
    while True:
        id_producto = solicitar_entero(
            "Ingrese el ID del producto: ", 1
        )

        for producto in productos:
            if producto.id_producto == id_producto:
                return producto

        print("[X] El ID ingresado no pertenece al listado.")


def solicitar_texto_actual(mensaje, valor_actual):
    valor = input(f"{mensaje} [{valor_actual}]: ").strip()

    if not valor:
        return valor_actual

    return valor


def solicitar_precio_actual(mensaje, valor_actual):
    texto = input(f"{mensaje} [{valor_actual}]: ").strip()

    if not texto:
        return valor_actual

    try:
        precio = Decimal(texto)

        if not precio.is_finite() or precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")

        if precio.as_tuple().exponent < -2:
            raise ValueError("El precio admite como máximo dos decimales.")

        if precio >= Decimal("100000000"):
            raise ValueError("El precio supera el máximo permitido.")

        return precio

    except InvalidOperation:
        raise ValueError("Debe ingresar un precio válido.")


def solicitar_entero_actual(mensaje, valor_actual, minimo=0):
    texto = input(f"{mensaje} [{valor_actual}]: ").strip()

    if not texto:
        return valor_actual

    try:
        valor = int(texto)

        if valor < minimo:
            raise ValueError(
                f"El valor debe ser igual o mayor que {minimo}."
            )

        return valor

    except ValueError:
        raise ValueError("Debe ingresar un número entero válido y positivo o cero.")


def seleccionar_relacion(
    registros,
    titulo,
    nombre_id,
    mensaje,
    id_actual=None
):
    if not registros:
        raise ValueError(
            f"No hay registros activos disponibles para {titulo.lower()}."
        )

    tabla = PrettyTable()
    tabla.field_names = ["ID", "Nombre"]

    for registro in registros:
        tabla.add_row([
            getattr(registro, nombre_id),
            registro.nombre
        ])

    print(f"\n--- {titulo} ---")
    print(tabla)

    if id_actual is not None:
        relacion_activa = False

        for registro in registros:
            if getattr(registro, nombre_id) == id_actual:
                relacion_activa = True
                break

        if relacion_activa:
            print(
                f"Presione ENTER para conservar el ID actual ({id_actual})."
            )
        else:
            print(
                "[!] La relación actual no está activa. "
                "Debe seleccionar otra."
            )

    while True:
        valor = input(mensaje).strip()

        if not valor and id_actual is not None:
            for registro in registros:
                if getattr(registro, nombre_id) == id_actual:
                    return id_actual

        if not valor.isdigit() or int(valor) <= 0:
            print("[X] Ingrese un ID válido.")
            continue

        id_seleccionado = int(valor)

        for registro in registros:
            if getattr(registro, nombre_id) == id_seleccionado:
                return id_seleccionado

        print("[X] El ID no pertenece al listado.")


def seleccionar_categoria(id_actual=None):
    categorias = listar_categorias_negocio()

    return seleccionar_relacion(
        categorias,
        "CATEGORÍAS ACTIVAS",
        "id_categoria",
        "Seleccione el ID de la categoría: ",
        id_actual
    )


def seleccionar_marca(id_actual=None):
    marcas = listar_marcas_negocio()

    return seleccionar_relacion(
        marcas,
        "MARCAS ACTIVAS",
        "id_marca",
        "Seleccione el ID de la marca: ",
        id_actual
    )


def seleccionar_proveedor(id_actual=None):
    proveedores = listar_proveedores_negocio()

    return seleccionar_relacion(
        proveedores,
        "PROVEEDORES ACTIVOS",
        "id_proveedor",
        "Seleccione el ID del proveedor: ",
        id_actual
    )


def presentacion_listado_producto():
    try:
        productos = listar_productos_negocio()
        mostrar_tabla_productos(productos, "LISTADO DE PRODUCTOS")

    except Exception:
        mostrar_error_general("Ocurrió un error al consultar los productos.")


def presentacion_listado_productos_desactivados(rol):
    try:
        productos = listar_productos_desactivados_negocio(rol)

        mostrar_tabla_productos(
            productos,
            "PRODUCTOS DESACTIVADOS"
        )

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general(
            "Ocurrió un error al consultar los productos desactivados."
        )


def presentacion_buscar_producto():
    try:
        id_producto = solicitar_entero(
            "Ingrese el ID del producto: ", 1
        )

        producto = buscar_producto_negocio(id_producto)

        print("\n--- INFORMACIÓN DEL PRODUCTO ---")
        print(f"ID: {producto.id_producto}")
        print(f"Nombre: {producto.nombre}")
        print(f"Descripción: {producto.descripcion}")
        print(f"Precio: ${producto.precio}")
        print(f"Stock: {producto.stock}")
        print(f"Stock mínimo: {producto.stock_minimo}")
        print(f"Categoría: {producto.nombre_categoria}")
        print(f"Marca: {producto.nombre_marca}")
        print(f"Proveedor: {producto.nombre_proveedor}")

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al buscar el producto.")


def presentacion_crear_producto(rol):
    print("\n--- CREAR NUEVO PRODUCTO ---")

    try:
        nombre = input("Ingrese el nombre: ").strip()
        descripcion = input("Ingrese la descripción: ").strip()

        precio = solicitar_precio("Ingrese el precio: ")

        stock = solicitar_entero("Ingrese el stock inicial: ")
        stock_minimo = solicitar_entero("Ingrese el stock mínimo: ")

        id_categoria = seleccionar_categoria()
        id_marca = seleccionar_marca()
        id_proveedor = seleccionar_proveedor()

        crear_producto_negocio(
            nombre,
            descripcion,
            precio,
            stock,
            stock_minimo,
            id_categoria,
            id_marca,
            id_proveedor,
            rol
        )

        print("\n[✔] Producto creado exitosamente.")

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al crear el producto.")


def solicitar_datos_actualizados(producto):
    print(f"\n--- MODIFICAR PRODUCTO: {producto.nombre} ---")
    print("Presione ENTER para conservar el dato actual.")

    nombre = solicitar_texto_actual(
        "Nuevo nombre", producto.nombre
    )

    descripcion = solicitar_texto_actual(
        "Nueva descripción", producto.descripcion
    )

    precio = solicitar_precio_actual(
        "Nuevo precio", producto.precio
    )

    stock_minimo = solicitar_entero_actual(
        "Nuevo stock mínimo",
        producto.stock_minimo
    )

    id_categoria = seleccionar_categoria(producto.id_categoria)
    id_marca = seleccionar_marca(producto.id_marca)
    id_proveedor = seleccionar_proveedor(producto.id_proveedor)

    return (
        nombre,
        descripcion,
        precio,
        stock_minimo,
        id_categoria,
        id_marca,
        id_proveedor
    )


def presentacion_actualizar_producto(rol):
    try:
        productos = listar_productos_negocio()

        if not mostrar_tabla_productos(
            productos,
            "PRODUCTOS DISPONIBLES PARA MODIFICAR"
        ):
            return

        producto = obtener_producto_seleccionado(productos)

        datos = solicitar_datos_actualizados(producto)

        (
            nombre,
            descripcion,
            precio,
            stock_minimo,
            id_categoria,
            id_marca,
            id_proveedor
        ) = datos

        if (
            nombre == producto.nombre
            and descripcion == producto.descripcion
            and Decimal(str(precio)) == Decimal(str(producto.precio))
            and stock_minimo == producto.stock_minimo
            and id_categoria == producto.id_categoria
            and id_marca == producto.id_marca
            and id_proveedor == producto.id_proveedor
        ):
            print("\nNo se realizaron cambios.")
            return

        actualizar_producto_negocio(
            producto.id_producto,
            *datos,
            rol
        )

        print("\n[✔] Producto actualizado exitosamente.")

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al actualizar el producto.")


def confirmar_operacion_producto(producto, accion):
    return solicitar_confirmacion(
        f"\n¿Está seguro de {accion} el producto "
        f"'{producto.nombre}'? (S/N): "
    )


def presentacion_eliminar_producto(rol):
    try:
        productos = listar_productos_negocio()

        if not mostrar_tabla_productos(
            productos,
            "PRODUCTOS ACTIVOS PARA DESACTIVAR"
        ):
            return

        producto = obtener_producto_seleccionado(productos)

        if not confirmar_operacion_producto(producto, "desactivar"):
            print("\nOperación cancelada.")
            return

        eliminar_producto_negocio(producto.id_producto, rol)

        print(
            f"\n[✔] Producto '{producto.nombre}' desactivado exitosamente."
        )

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al desactivar el producto.")


def presentacion_reactivar_producto(rol):
    try:
        productos = listar_productos_desactivados_negocio(rol)

        if not mostrar_tabla_productos(
            productos,
            "PRODUCTOS DISPONIBLES PARA REACTIVAR"
        ):
            return

        producto = obtener_producto_seleccionado(productos)

        if not confirmar_operacion_producto(producto, "reactivar"):
            print("\nOperación cancelada.")
            return

        reactivar_producto_negocio(producto.id_producto, rol)

        print(
            f"\n[✔] Producto '{producto.nombre}' reactivado exitosamente."
        )

    except (ValueError, PermissionError) as e:
        mostrar_error(e)

    except Exception:
        mostrar_error_general("Ocurrió un error al reactivar el producto.")


def menu_productos(usuario_actual):
    rol = usuario_actual.rol if usuario_actual else None

    es_admin = (
        isinstance(rol, str)
        and rol.strip().upper() == "ADMINISTRADOR"
    )

    while True:
        print("\n===== GESTIÓN DE PRODUCTOS =====")
        print("1. Listar productos")
        print("2. Buscar producto por ID")

        if es_admin:
            print("3. Crear producto")
            print("4. Actualizar producto")
            print("5. Desactivar producto")
            print("6. Listar productos desactivados")
            print("7. Reactivar producto")
            print("8. Volver al menú principal")
        else:
            print("3. Volver al menú principal")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            presentacion_listado_producto()

        elif opcion == "2":
            presentacion_buscar_producto()

        elif opcion == "3" and es_admin:
            presentacion_crear_producto(rol)

        elif opcion == "4" and es_admin:
            presentacion_actualizar_producto(rol)

        elif opcion == "5" and es_admin:
            presentacion_eliminar_producto(rol)

        elif opcion == "6" and es_admin:
            presentacion_listado_productos_desactivados(rol)

        elif opcion == "7" and es_admin:
            presentacion_reactivar_producto(rol)

        elif opcion == "8" and es_admin:
            break

        elif opcion == "3" and not es_admin:
            break

        else:
            print("\n[X] Opción no válida o sin permisos.")






