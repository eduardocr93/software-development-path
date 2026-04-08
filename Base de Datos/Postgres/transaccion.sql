INSERT INTO usuarios (nombre, email)
VALUES ('Ana', 'ana@mail.com'),
       ('Luis', 'luis@mail.com');

SELECT * FROM usuarios;

INSERT INTO productos (nombre, stock, precio)
VALUES ('Laptop', 10, 800.00),
       ('Mouse', 50, 20.00);


SELECT * FROM productos;


DO $$
DECLARE
    v_usuario_id INT := 1;       -- Usuario Ana
    v_producto_id INT := 1;      -- Laptop
    v_cantidad INT := 2;         -- Compra de 2 laptops
    v_stock_actual INT;
    v_precio NUMERIC(10,2);
    v_factura_id INT;
BEGIN
    -- Validar usuario
    IF NOT EXISTS (SELECT 1 FROM usuarios WHERE id = v_usuario_id) THEN
        RAISE EXCEPTION 'Usuario no existe';
    END IF;

    -- Validar stock
    SELECT stock, precio INTO v_stock_actual, v_precio
    FROM productos WHERE id = v_producto_id;

    IF v_stock_actual IS NULL THEN
        RAISE EXCEPTION 'Producto no existe';
    END IF;

    IF v_stock_actual < v_cantidad THEN
        RAISE EXCEPTION 'Stock insuficiente';
    END IF;

    -- Crear factura
    INSERT INTO facturas (usuario_id) VALUES (v_usuario_id)
    RETURNING id INTO v_factura_id;

    -- Insertar detalle
    INSERT INTO factura_detalle (factura_id, producto_id, cantidad, precio_unitario)
    VALUES (v_factura_id, v_producto_id, v_cantidad, v_precio);

    -- Actualizar stock
    UPDATE productos SET stock = stock - v_cantidad
    WHERE id = v_producto_id;

    RAISE NOTICE 'Compra realizada con éxito. Factura % creada.', v_factura_id;
END;
$$;

SELECT * FROM facturas;

SELECT * FROM factura_detalle;

SELECT * FROM productos;

SELECT * FROM usuarios;



