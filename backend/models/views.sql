-- Vista de stock actual por variante y estado. Se calcula siempre a
-- partir de movimientos_inventario (ver backend/models/inventario.py),
-- nunca se guarda como campo editable en ninguna tabla.
--
-- Correr este script una vez despues de Base.metadata.create_all(),
-- ya que SQLAlchemy no crea vistas automaticamente.

CREATE VIEW IF NOT EXISTS vista_stock_actual AS
SELECT
    variante_id,
    estado,
    SUM(cantidad) AS saldo
FROM (
    SELECT variante_id, estado_destino AS estado, cantidad
    FROM movimientos_inventario
    WHERE estado_destino IS NOT NULL

    UNION ALL

    SELECT variante_id, estado_origen AS estado, -cantidad
    FROM movimientos_inventario
    WHERE estado_origen IS NOT NULL
) AS movimientos_por_estado
GROUP BY variante_id, estado;
