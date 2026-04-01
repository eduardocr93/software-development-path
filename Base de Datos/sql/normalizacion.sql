-- Problemas:
-- - Se repite el cliente (Alice) varias veces
-- - Se repiten datos del producto
-- - Difícil de mantener (si cambia teléfono hay que actualizar muchas filas)

-- 1FN (Primera Forma Normal)
-- Ya está parcialmente cumplida porque cada fila tiene valores atómicos
-- Cada producto está en una fila distinta

-- 2FN (Segunda Forma Normal)
-- Problema:
-- La clave sería (OrderID + ItemID)
-- Pero:
-- - CustomerName depende solo de OrderID
-- - ItemName depende solo de ItemID
--Solución: separar en tablas independientes

-- 3FN (Tercera Forma Normal)
-- Problema:
-- - CustomerName determina Phone
-- - CustomerName determina Address
--Solución: separar clientes en otra tabla


-- Aquí se guarda información única del cliente
-- Ejemplo: Alice solo aparece una vez
CREATE TABLE clientes (
    customer_id INTEGER PRIMARY KEY,
    nombre TEXT,
    telefono TEXT
);


-- Cada orden pertenece a un cliente
-- Ya no repetimos nombre ni teléfono
CREATE TABLE ordenes (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    direccion TEXT,
    hora_entrega TEXT,
    FOREIGN KEY (customer_id) REFERENCES clientes(customer_id)
);


-- Productos independientes
-- Ejemplo: Fries existe una sola vez
CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    nombre TEXT,
    precio REAL
);


-- Relaciona órdenes con productos
-- Ejemplo:
-- Orden 001 → Cheeseburger x2
-- Orden 001 → Fries x1
CREATE TABLE orden_detalle (
    order_id INTEGER,
    item_id INTEGER,
    cantidad INTEGER,
    solicitud_especial TEXT,
    PRIMARY KEY (order_id, item_id),
    FOREIGN KEY (order_id) REFERENCES ordenes(order_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);




-- Problemas:
-- - Un carro puede tener varios dueños
-- - Se repiten datos del vehículo
-- - Se repiten datos del seguro

-- 2FN
-- Problema:
-- - Make, Model dependen solo de VIN
-- - OwnerName depende solo de OwnerID
--
--  Solución: separar entidades


-- 3FN
-- Problema:
-- - InsuranceCompany determina Policy
--
-- Solución: separar seguros

CREATE TABLE modelos (
    modelo_id INTEGER PRIMARY KEY,
    marca TEXT,
    modelo TEXT
);

CREATE TABLE vehiculos (
    vin TEXT PRIMARY KEY,
    modelo_id INTEGER,
    anio INTEGER,
    color TEXT,
    FOREIGN KEY (modelo_id) REFERENCES modelos(modelo_id)
);

-- Información de personas
CREATE TABLE propietarios (
    owner_id INTEGER PRIMARY KEY,
    nombre TEXT,
    telefono TEXT
);

-- Un carro puede tener varios dueños
CREATE TABLE vehiculo_propietario (
    vin TEXT,
    owner_id INTEGER,
    PRIMARY KEY (vin, owner_id),
    FOREIGN KEY (vin) REFERENCES vehiculos(vin),
    FOREIGN KEY (owner_id) REFERENCES propietarios(owner_id)
);

CREATE TABLE companias (
    compania_id INTEGER PRIMARY KEY,
    nombre TEXT
);

CREATE TABLE tipos_seguro (
    tipo_id INTEGER PRIMARY KEY,
    descripcion TEXT
);

CREATE TABLE polizas (
    policy_id TEXT PRIMARY KEY,
    compania_id INTEGER,
    tipo_id INTEGER,
    FOREIGN KEY (compania_id) REFERENCES companias(compania_id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_seguro(tipo_id)
);

-- Relaciona carro con su póliza
CREATE TABLE vehiculo_seguro (
    vin TEXT,
    policy_id TEXT,
    PRIMARY KEY (vin, policy_id),
    FOREIGN KEY (vin) REFERENCES vehiculos(vin),
    FOREIGN KEY (policy_id) REFERENCES polizas(policy_id)
);

INSERT INTO clientes (customer_id, nombre, telefono) VALUES
(1, 'Alice', '123-456-7890'),
(2, 'Bob', '987-654-3210'),
(3, 'Claire', '555-123-4567');


INSERT INTO ordenes (order_id, customer_id, direccion, hora_entrega) VALUES
(1, 1, '123 Main St', '6:00 PM'),
(2, 2, '456 Elm St', '7:30 PM'),
(3, 3, '789 Oak St', '12:00 PM'),
(4, 3, '464 Georgia St', '5:00 PM');


INSERT INTO items (item_id, nombre, precio) VALUES
(101, 'Cheeseburger', 8),
(102, 'Fries', 3),
(103, 'Pizza', 12),
(105, 'Salad', 6),
(106, 'Water', 1);


INSERT INTO orden_detalle (order_id, item_id, cantidad, solicitud_especial) VALUES
(1, 101, 2, 'No onions'),
(1, 102, 1, 'Extra ketchup'),
(2, 103, 1, 'Extra cheese'),
(2, 102, 2, 'None'),
(3, 105, 1, 'No croutons'),
(4, 106, 1, 'None');

INSERT INTO modelos (modelo_id, marca, modelo) VALUES
(1, 'Honda', 'Accord'),
(2, 'Honda', 'CR-V'),
(3, 'Chevrolet', 'Volt');


INSERT INTO vehiculos (vin, modelo_id, anio, color) VALUES
('1HGCM82633A', 1, 2003, 'Silver'),
('5J6RM4H79EL', 2, 2014, 'Blue'),
('1G1RA6EH1FU', 3, 2015, 'Red');


INSERT INTO propietarios (owner_id, nombre, telefono) VALUES
(101, 'Alice', '123-456-7890'),
(102, 'Bob', '987-654-3210'),
(103, 'Claire', '555-123-4567'),
(104, 'Dave', '111-222-3333');

INSERT INTO vehiculo_propietario (vin, owner_id) VALUES
('1HGCM82633A', 101),
('1HGCM82633A', 102),
('5J6RM4H79EL', 103),
('1G1RA6EH1FU', 104);

INSERT INTO companias (compania_id, nombre) VALUES
(1, 'ABC Insurance'),
(2, 'XYZ Insurance'),
(3, 'DEF Insurance'),
(4, 'GHI Insurance');


INSERT INTO tipos_seguro (tipo_id, descripcion) VALUES
(1, 'Seguro completo'),
(2, 'Seguro contra robo'),
(3, 'Seguro contra choque');


INSERT INTO polizas (policy_id, compania_id, tipo_id) VALUES
('POL12345', 1, 1),
('POL54321', 2, 2),
('POL67890', 3, 1),
('POL98765', 4, 3);

INSERT INTO vehiculo_seguro (vin, policy_id) VALUES
('1HGCM82633A', 'POL12345'),
('1HGCM82633A', 'POL54321'),
('5J6RM4H79EL', 'POL67890'),
('1G1RA6EH1FU', 'POL98765');
