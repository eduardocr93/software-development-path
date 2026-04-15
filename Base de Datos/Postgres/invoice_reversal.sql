DO $$
DECLARE
    v_invoice_id INT := 1;   -- ID de la factura que quieres devolver
    rec RECORD;
BEGIN
    -- Validar factura
    IF NOT EXISTS (SELECT 1 FROM invoices WHERE id = v_invoice_id) THEN
        RAISE EXCEPTION 'Invoice does not exist';
    END IF;

    -- Validar que no esté ya retornada
    IF EXISTS (SELECT 1 FROM invoices WHERE id = v_invoice_id AND status = 'Returned') THEN
        RAISE EXCEPTION 'Invoice already returned';
    END IF;

    -- Recorrer todos los productos del detalle
    FOR rec IN SELECT product_id, quantity FROM invoice_details WHERE invoice_id = v_invoice_id LOOP
        UPDATE products SET stock = stock + rec.quantity
        WHERE id = rec.product_id;
    END LOOP;

    -- Marcar factura como retornada
    UPDATE invoices SET status = 'Returned'
    WHERE id = v_invoice_id;

    RAISE NOTICE 'Invoice % marked as returned and stock restored.', v_invoice_id;
END;
$$;