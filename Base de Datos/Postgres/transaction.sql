DO $$
DECLARE
    v_user_id INT := 1;        -- Usuario que compra
    v_product_id INT := 1;     -- Producto a comprar
    v_quantity INT := 2;       -- Cantidad
    v_stock INT;
    v_price NUMERIC(10,2);
    v_invoice_id INT;
BEGIN
    -- Validar usuario
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = v_user_id) THEN
        RAISE EXCEPTION 'User does not exist';
    END IF;

    -- Validar stock
    SELECT stock, price INTO v_stock, v_price
    FROM products WHERE id = v_product_id;

    IF v_stock IS NULL THEN
        RAISE EXCEPTION 'Product does not exist';
    END IF;

    IF v_stock < v_quantity THEN
        RAISE EXCEPTION 'Insufficient stock';
    END IF;

    -- Crear factura
    INSERT INTO invoices (user_id) VALUES (v_user_id)
    RETURNING id INTO v_invoice_id;

    -- Insertar detalle
    INSERT INTO invoice_details (invoice_id, product_id, quantity, unit_price)
    VALUES (v_invoice_id, v_product_id, v_quantity, v_price);

    -- Actualizar stock
    UPDATE products SET stock = stock - v_quantity
    WHERE id = v_product_id;

    RAISE NOTICE 'Purchase successful. Invoice % created.', v_invoice_id;
END;
$$;