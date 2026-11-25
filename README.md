# TiendaInline – Aplicación de consola para tienda online (e-commerce)

Aplicación multicapa en Python con persistencia en MySQL mediante el ORM **Peewee**, contraseñas protegidas con **BCrypt**, login y menú principal según el rol del usuario.
Corresponde a la continuación del proyecto de la Evaluación N°2 (Programación Orientada a Objetos).

## Integrantes

Nombre completo  	Rol en el proyecto

Berhane Castro :  Desarrollo del proyecto


Profesor:Erick Bailey Rebolledo


Sección: IEI-N2-C2/D 

## Descripción general

TiendaInline simula el back‑office y el flujo de compra de una tienda online desde la terminal. Gestiona el catálogo (categorías, marcas, proveedores, productos e imágenes), el inventario, carritos, pedidos, pagos, cupones de descuento, direcciones y valoraciones de productos. El acceso exige iniciar sesión y las opciones del menú cambian según el rol del usuario (`ADMINISTRADOR` o `CLIENTE`).

## Funcionalidades principales

- **Login obligatorio** con correo y contraseña (la contraseña se ingresa oculta con `maskpass`).
- **Contraseñas con BCrypt**: solo se almacena el hash (`password_hash`).
- **Gestión de usuarios** (administrador): registrar, listar, modificar, desactivar y reactivar. Incluye validación de RUT chileno, correo, teléfono y contraseña segura (mínimo 8 caracteres, mayúscula, minúscula, número y carácter especial).
- **CRUD con baja lógica** (campo `activo`) de categorías, marcas, proveedores, productos, imágenes de producto, direcciones, formas de pago, cupones y valoraciones.
- **Stock**: movimientos de stock por producto (administrador).
- **Carrito de compras** por cliente y gestión de carritos (administrador).
- **Pedidos**: finalización de compra (checkout, con bloqueo de fila para el stock), historial, detalle y cancelación de pedidos pendientes (devuelve el stock y rechaza los pagos).
- **Pagos**: consulta por ID o por pedido y actualización de estado (administrador).
- **Menú por rol**: cada opción se muestra solo a todos, solo a administradores o solo a clientes.

## Tecnologías y dependencias

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje (los `.pyc` del proyecto fueron generados con 3.12) |
| MySQL / MariaDB (InnoDB, utf8mb4) | Base de datos `tienda_online` |
| [Peewee](https://docs.peewee-orm.com/) | ORM y persistencia (claves foráneas con `ForeignKeyField`) |
| PyMySQL | Driver de conexión a MySQL |
| python-decouple | Lectura de la configuración desde `.env` |
| bcrypt | Hash y verificación de contraseñas |
| prettytable | Tablas en consola |
| maskpass | Ocultar la contraseña al escribirla |

Todas están listadas en `requirements.txt`.

## Arquitectura y estructura de carpetas

Arquitectura por capas: **presentación → negocio → datos**, con una capa de **auxiliares** transversal.

```
proyecto/
├── main.py                         # Punto de entrada
├── crear_admin.py                  # Crea el administrador inicial (se ejecuta una vez)
├── requirements.txt                # Dependencias
├── .env.example                    # Plantilla de configuración (copiar como .env)
├── .gitignore
├── README.md
├── docs/
│   ├── diagrama_uml.mmd            # Diagrama UML (Mermaid, editable)
│   ├── diagrama_uml.png
│   └── diagrama_uml.svg
├── datos/                          # Persistencia
│   ├── conexion.py                 # Conexión a MySQL (DB)
│   ├── model_base.py               # ModelBase: configuración compartida por los modelos
│   ├── modelos/                    # 16 modelos Peewee (heredan de ModelBase)
│   ├── repositorio/                # Funciones de acceso a datos (repo_*.py)
│   └── sql/
│       └── tienda_online.sql       # Script de creación de la base y las 16 tablas
├── negocio/                        # Reglas de negocio y validaciones (*_negocio.py)
├── presentacion/                   # Menús y captura de datos (*_presentacion.py, menu.py)
└── auxiliares/                     # Constantes y configuración (datos_app.py)
```

| Capa | Responsabilidad |
|---|---|
| `datos` | Conexión, `ModelBase`, modelos ORM, repositorios (funciones de guardado con `save()`, listado y búsquedas) y scripts SQL |
| `negocio` | Reglas de negocio, validaciones y coordinación entre presentación y datos |
| `presentacion` | Interacción con el usuario: menús, captura de datos y presentación de resultados |
| `auxiliares` | Constantes, mensajes y validaciones reutilizables (p. ej. `validar_administrador`, `es_administrador`) |

## Instalación de dependencias

Requisitos previos: **Python 3.12** y **MySQL Server 8.x** (o MariaDB) instalados.

```bash
# 1. Entrar a la carpeta del proyecto
cd proyecto

# 2. (Recomendado) crear y activar un entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Configuración de MySQL

1. Asegúrate de que el servicio de MySQL esté en ejecución.
2. Ingresa al cliente de MySQL con un usuario con permisos para crear bases de datos (el script SQL crea `tienda_online`):

   ```bash
   mysql -u root -p
   ```

3. (Opcional, recomendado) crea un usuario dedicado para la aplicación. Ejecútalo **después** de importar el script, para que la base ya exista:

   ```sql
   CREATE USER 'tienda_user'@'localhost' IDENTIFIED BY 'TuClaveSegura';
   GRANT ALL PRIVILEGES ON tienda_online.* TO 'tienda_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

## Creación e importación de la base de datos

El script `datos/sql/tienda_online.sql` crea la base de datos `tienda_online` (si no existe, con `utf8mb4`) y las 16 tablas. Desde la raíz del proyecto:

```bash
mysql -u root -p < datos/sql/tienda_online.sql
```

> En Windows PowerShell el operador `<` no funciona; usa `cmd`, o bien dentro del cliente MySQL: `SOURCE datos/sql/tienda_online.sql;`

Se crean **16 tablas** con **17 claves foráneas**: `usuario`, `direccion`, `categoria`, `marca`, `proveedor`, `producto`, `imagen_producto`, `movimiento_stock`, `carrito`, `detalle_carrito`, `cupon`, `pedido`, `detalle_pedido`, `forma_pago`, `pago`, `valoracion`.

Para verificar:

```sql
USE tienda_online;
SHOW TABLES;
```

> El script no borra tablas existentes. Si necesitas reimportarlo, elimina antes la base: `DROP DATABASE tienda_online;`

## Configuración de conexión

La conexión se define en `datos/conexion.py`, que lee la variable `DATABASE` desde un archivo `.env` ubicado en la **raíz del proyecto**:

```python
DB = connect(config('DATABASE'))
```

Crea el archivo `.env` (puedes copiar `.env.example`):

```env
DATABASE=mysql://tienda_user:TuClaveSegura@localhost:3306/tienda_online
```

Formato: `mysql://USUARIO:CLAVE@HOST:PUERTO/BASE_DE_DATOS`. Si la clave contiene caracteres especiales (`@`, `:`, `/`), codifícalos en formato URL (por ejemplo `@` → `%40`).

> No subas el archivo `.env` al repositorio (agrégalo a `.gitignore`).

## Ejecución del programa

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
python main.py
```

Aparece la pantalla de inicio de sesión; tras autenticarse se muestra el menú principal según el rol.

## Usuario inicial

El script SQL **no inserta usuarios**, y la pantalla inicial solo permite iniciar sesión (los usuarios que se registran desde el menú de administración quedan con rol `CLIENTE`). Por eso, la primera vez hay que crear el administrador con el script incluido. Con la base importada y el `.env` configurado, desde la raíz del proyecto:

```bash
python crear_admin.py
```

Credenciales iniciales:

| Campo | Valor |
|---|---|
| Correo | `admin@tienda.cl` |
| Contraseña | `Admin.2026` |
| Rol | `ADMINISTRADOR` |

La contraseña se guarda cifrada con BCrypt. El script es seguro de repetir: si el administrador ya existe, no hace nada. Con la sesión de administrador se pueden registrar más usuarios desde **Gestión de usuarios → Registrar usuario**.

## Diagrama UML de clases

El diagrama representa los **16 modelos** (que heredan de `ModelBase`), con atributos, tipos, identificadores, relaciones y cardinalidades contrastadas con el script SQL. Cada clase incluye también sus **operaciones** (guardar, obtener, listar, actualizar, eliminar, etc.), que corresponden a las funciones de su repositorio y de la capa de negocio (se omite el sufijo `_repo` en el nombre).

![Diagrama UML](docs/diagrama_uml.png)

Versión editable (Mermaid): [`docs/diagrama_uml.mmd`](docs/diagrama_uml.mmd). Versión vectorial: [`docs/diagrama_uml.svg`](docs/diagrama_uml.svg).

Resumen de relaciones (según las claves foráneas del SQL):

| Relación | Cardinalidad | Observación |
|---|---|---|
| Usuario → Dirección | 1 a 0..* | |
| Usuario → Carrito | 1 a 0..1 | `id_usuario` es `UNIQUE` en `carrito` |
| Usuario → Pedido | 1 a 0..* | |
| Usuario → Valoración | 1 a 0..* | Único por (`id_usuario`, `id_producto`) |
| Categoría / Marca / Proveedor → Producto | 1 a 0..* | |
| Producto → ImagenProducto / MovimientoStock / Valoración | 1 a 0..* | |
| Carrito → DetalleCarrito | 1 a 0..* | Composición (`ON DELETE CASCADE`) |
| Pedido → DetallePedido | 1 a 0..* | |
| Producto → DetalleCarrito / DetallePedido | 1 a 0..* | |
| Cupón → Pedido | 0..1 a 0..* | `id_cupon` admite `NULL` |
| Pedido → Pago | 1 a 0..* | |
| FormaPago → Pago | 1 a 0..* | |
