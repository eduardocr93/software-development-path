DO $$
DECLARE
    v_factura_id INT := 1;   -- ID de la factura que quieres devolver
    v_producto_id INT;
    v_cantidad INT;
BEGIN
    -- Verificar que la factura existe
    IF NOT EXISTS (SELECT 1 FROM facturas WHERE id = v_factura_id) THEN
        RAISE EXCEPTION 'Factura no existe';
    END IF;

    -- Obtener detalle de la factura
    SELECT producto_id, cantidad INTO v_producto_id, v_cantidad
    FROM factura_detalle WHERE factura_id = v_factura_id LIMIT 1;

    IF v_producto_id IS NULL THEN
        RAISE EXCEPTION 'Factura sin detalle';
    END IF;

    -- Devolver stock
    UPDATE productos SET stock = stock + v_cantidad
    WHERE id = v_producto_id;

    -- Marcar factura como retornada
    UPDATE facturas SET estado = 'Retornada'
    WHERE id = v_factura_id;

    RAISE NOTICE 'Factura % marcada como retornada y stock actualizado.', v_factura_id;
END;
$$;

SELECT * FROM facturas;
SELECT * FROM productos;