CREATE DATABASE IF NOT EXISTS tienda_online_test
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE tienda_online_test;

-- =====================================================
-- PROYECTO E-COMMERCE
-- MOTOR: InnoDB
-- CHARSET: utf8mb4
-- COLLATION: utf8mb4_unicode_ci
-- =====================================================


-- =============================================
-- 1. TABLA USUARIO
-- =============================================

CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    rut VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NULL,
    rol VARCHAR(30) NOT NULL DEFAULT 'CLIENTE',
    fecha_nacimiento DATE NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 2. TABLA DIRECCION
-- =============================================

CREATE TABLE direccion (
    id_direccion INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    calle VARCHAR(150) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    comuna VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(20) NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,

    INDEX idx_direccion_usuario (id_usuario),

    CONSTRAINT fk_direccion_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario(id_usuario)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 3. TABLA CATEGORIA
-- =============================================

CREATE TABLE categoria (
    id_categoria INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 4. TABLA MARCA
-- =============================================

CREATE TABLE marca (
    id_marca INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    activo TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 5. TABLA PROVEEDOR
-- =============================================

CREATE TABLE proveedor (
    id_proveedor INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    rut VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    activo TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 6. TABLA PRODUCTO
-- =============================================

CREATE TABLE producto (
    id_producto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    stock_minimo INT NOT NULL DEFAULT 0,
    id_categoria INT NOT NULL,
    id_marca INT NOT NULL,
    id_proveedor INT NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) NOT NULL DEFAULT 1,

    INDEX idx_producto_categoria (id_categoria),
    INDEX idx_producto_marca (id_marca),
    INDEX idx_producto_proveedor (id_proveedor),

    CONSTRAINT chk_producto_precio
    CHECK (precio >= 0),

    CONSTRAINT chk_producto_stock
    CHECK (stock >= 0),

    CONSTRAINT chk_producto_stock_minimo
    CHECK (stock_minimo >= 0),

    CONSTRAINT fk_producto_categoria
    FOREIGN KEY (id_categoria)
    REFERENCES categoria(id_categoria)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    CONSTRAINT fk_producto_marca
    FOREIGN KEY (id_marca)
    REFERENCES marca(id_marca)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    CONSTRAINT fk_producto_proveedor
    FOREIGN KEY (id_proveedor)
    REFERENCES proveedor(id_proveedor)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 7. TABLA IMAGEN_PRODUCTO
-- =============================================

CREATE TABLE imagen_producto (
    id_imagen INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    url_imagen VARCHAR(255) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,

    INDEX idx_imagen_producto (id_producto),

    CONSTRAINT fk_imagen_producto
    FOREIGN KEY (id_producto)
    REFERENCES producto(id_producto)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 8. TABLA MOVIMIENTO_STOCK
-- =============================================

CREATE TABLE movimiento_stock (
    id_movimiento INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    fecha_movimiento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_movimiento_producto (id_producto),

    CONSTRAINT chk_movimiento_cantidad
    CHECK (cantidad > 0),

    CONSTRAINT fk_movimiento_producto
    FOREIGN KEY (id_producto)
    REFERENCES producto(id_producto)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 9. TABLA CARRITO
-- =============================================

CREATE TABLE carrito (
    id_carrito INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    activo TINYINT(1) NOT NULL DEFAULT 1,

    CONSTRAINT fk_carrito_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario(id_usuario)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 10. TABLA DETALLE_CARRITO
-- =============================================

CREATE TABLE detalle_carrito (
    id_detalle_carrito INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_carrito INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,

    UNIQUE KEY uq_detalle_carrito_producto (id_carrito, id_producto),
    INDEX idx_detalle_carrito_producto (id_producto),

    CONSTRAINT chk_detalle_carrito_cantidad
    CHECK (cantidad > 0),

    CONSTRAINT chk_detalle_carrito_precio
    CHECK (precio_unitario >= 0),

    CONSTRAINT chk_detalle_carrito_subtotal
    CHECK (subtotal >= 0),

    CONSTRAINT fk_detalle_carrito
    FOREIGN KEY (id_carrito)
    REFERENCES carrito(id_carrito)
    ON DELETE CASCADE
    ON UPDATE CASCADE,

    CONSTRAINT fk_detalle_carrito_producto
    FOREIGN KEY (id_producto)
    REFERENCES producto(id_producto)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 11. TABLA CUPON
-- =============================================

CREATE TABLE cupon (
    id_cupon INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    descuento DECIMAL(5,2) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1,

    CONSTRAINT chk_cupon_descuento
    CHECK (descuento > 0 AND descuento <= 100),

    CONSTRAINT chk_cupon_fechas
    CHECK (fecha_fin >= fecha_inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 12. TABLA PEDIDO
-- =============================================

CREATE TABLE pedido (
    id_pedido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_cupon INT NULL,
    direccion_envio VARCHAR(300) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE',
    total DECIMAL(10,2) NOT NULL,
    fecha_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_pedido_usuario (id_usuario),
    INDEX idx_pedido_cupon (id_cupon),

    CONSTRAINT chk_pedido_total
    CHECK (total >= 0),

    CONSTRAINT fk_pedido_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario(id_usuario)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    CONSTRAINT fk_pedido_cupon
    FOREIGN KEY (id_cupon)
    REFERENCES cupon(id_cupon)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 13. TABLA DETALLE_PEDIDO
-- =============================================

CREATE TABLE detalle_pedido (
    id_detalle INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,

    UNIQUE KEY uq_detalle_pedido_producto (id_pedido, id_producto),
    INDEX idx_detalle_pedido_producto (id_producto),

    CONSTRAINT chk_detalle_pedido_cantidad
    CHECK (cantidad > 0),

    CONSTRAINT chk_detalle_pedido_precio
    CHECK (precio_unitario >= 0),

    CONSTRAINT chk_detalle_pedido_subtotal
    CHECK (subtotal >= 0),

    CONSTRAINT fk_detalle_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido(id_pedido)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    CONSTRAINT fk_detalle_pedido_producto
    FOREIGN KEY (id_producto)
    REFERENCES producto(id_producto)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 14. TABLA FORMA_PAGO
-- =============================================

CREATE TABLE forma_pago (
    id_forma_pago INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255) NOT NULL,
    activo TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 15. TABLA PAGO
-- =============================================

CREATE TABLE pago (
    id_pago INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_forma_pago INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE',
    fecha_pago TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_pago_pedido (id_pedido),
    INDEX idx_pago_forma_pago (id_forma_pago),

    CONSTRAINT chk_pago_monto
    CHECK (monto > 0),

    CONSTRAINT fk_pago_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido(id_pedido)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    CONSTRAINT fk_pago_forma_pago
    FOREIGN KEY (id_forma_pago)
    REFERENCES forma_pago(id_forma_pago)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- 16. TABLA VALORACION
-- =============================================

CREATE TABLE valoracion (
    id_valoracion INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_producto INT NOT NULL,
    puntuacion INT NOT NULL,
    comentario VARCHAR(500) NULL,
    fecha_valoracion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    activo TINYINT(1) NOT NULL DEFAULT 1,

    UNIQUE KEY uq_valoracion_usuario_producto (id_usuario, id_producto),
    INDEX idx_valoracion_usuario (id_usuario),
    INDEX idx_valoracion_producto (id_producto),

    CONSTRAINT chk_valoracion_puntuacion
    CHECK (puntuacion BETWEEN 1 AND 5),

    CONSTRAINT fk_valoracion_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario(id_usuario)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    CONSTRAINT fk_valoracion_producto
    FOREIGN KEY (id_producto)
    REFERENCES producto(id_producto)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================
-- FIN DE LA BASE DE DATOS
-- 16 TABLAS
-- 17 CLAVES FORANEAS
-- =============================================
