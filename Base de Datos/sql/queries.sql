-- SQLite tiene una limitante:
-- AUTO_INCREMENT no existe como en MySQL
-- Se usa: INTEGER PRIMARY KEY AUTOINCREMENT

-- PRODUCTOS
CREATE TABLE productos (
    codigo TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL CHECK (precio > 0),
    fecha_ingreso DATE,
    marca TEXT
);

-- FACTURAS
CREATE TABLE facturas (
    numero_factura INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_compra DATE NOT NULL,
    correo_comprador TEXT NOT NULL,
    telefono TEXT,
    codigo_empleado TEXT,
    monto_total REAL
);

-- DETALLE FACTURA
CREATE TABLE detalle_factura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_factura INTEGER,
    codigo_producto TEXT,
    cantidad INTEGER NOT NULL,
    monto_total REAL,
    FOREIGN KEY (numero_factura) REFERENCES facturas(numero_factura),
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo)
);

-- CARRITO
CREATE TABLE carrito (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo_usuario TEXT
);

-- CARRITO_PRODUCTO
CREATE TABLE carrito_producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_carrito INTEGER,
    codigo_producto TEXT,
    cantidad INTEGER,
    FOREIGN KEY (id_carrito) REFERENCES carrito(id),
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo)
);

INSERT INTO productos VALUES ('P01', 'Laptop', 60000, '2026-01-01', 'Dell');
INSERT INTO productos VALUES ('P02', 'Mouse', 10000, '2026-01-02', 'Logitech');

INSERT INTO facturas (fecha_compra, correo_comprador, telefono, codigo_empleado, monto_total)
VALUES ('2026-03-20', 'test@gmail.com', '88888888', 'EMP01', 70000);

INSERT INTO detalle_factura (numero_factura, codigo_producto, cantidad, monto_total)
VALUES (1, 'P01', 1, 60000);

INSERT INTO detalle_factura (numero_factura, codigo_producto, cantidad, monto_total)
VALUES (1, 'P02', 1, 10000);

SELECT * FROM productos;

SELECT * 
FROM productos
WHERE precio > 50000;

SELECT * 
FROM detalle_factura
WHERE codigo_producto = 'P01';

SELECT 
    codigo_producto,
    SUM(cantidad) AS total_comprado
FROM detalle_factura
GROUP BY codigo_producto;

SELECT *
FROM facturas
WHERE correo_comprador = 'test@gmail.com';

SELECT *
FROM facturas
ORDER BY monto_total DESC;

SELECT *
FROM facturas
WHERE numero_factura = 1;