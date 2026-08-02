"""Depositos, movimientos de inventario y pedidos sin stock (backorder).

El estado de stock de una variante (en_stock, reservado, en_reparacion,
vendido, perdido) NUNCA se guarda como campo editable en ningun lado:
se calcula siempre a partir de la suma de movimientos_inventario. Ver
backend/models/views.sql para la vista de solo lectura que resuelve
ese calculo (vista_stock_actual).
"""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base

# Tipos de movimiento soportados y su efecto sobre estado_origen /
# estado_destino (documentado en docs/ADR.md al agregar el ADR
# correspondiente):
#   compra                -> (ninguno) a en_stock
#   venta                 -> en_stock a vendido
#   reserva                -> en_stock a reservado
#   liberacion_reserva     -> reservado a en_stock
#   venta_de_reservado     -> reservado a vendido
#   envio_reparacion       -> en_stock a en_reparacion
#   retorno_reparacion     -> en_reparacion a en_stock
#   perdida                -> en_stock a perdido
#   devolucion_cliente     -> vendido a en_stock
#   devolucion_proveedor   -> en_stock a (ninguno)
#   ajuste                 -> en_stock o (ninguno) a en_stock, signado
#   transferencia          -> en_stock a en_stock (otro deposito)
TIPOS_MOVIMIENTO = (
    "compra",
    "venta",
    "reserva",
    "liberacion_reserva",
    "venta_de_reservado",
    "envio_reparacion",
    "retorno_reparacion",
    "perdida",
    "devolucion_cliente",
    "devolucion_proveedor",
    "ajuste",
    "transferencia",
)

ESTADOS_STOCK = ("en_stock", "reservado", "en_reparacion", "vendido", "perdido")


class Deposito(Base):
    """Ubicacion fisica de stock. Hoy arranca con un solo registro
    semilla ("Principal"); preparado para agregar mas en el futuro sin
    migrar el resto del modelo.
    """

    __tablename__ = "depositos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class MovimientoInventario(Base):
    """Ledger de movimientos de stock. Cada fila mueve `cantidad`
    unidades de `estado_origen` a `estado_destino` (alguno puede ser
    nulo: entrada o salida definitiva de la variante).

    referencia_tipo / referencia_id apuntan opcionalmente a la compra o
    venta que origino el movimiento (ej. referencia_tipo="compra",
    referencia_id=compras.id), sin usar una FK polimorfica formal.
    """

    __tablename__ = "movimientos_inventario"

    id: Mapped[int] = mapped_column(primary_key=True)
    variante_id: Mapped[int] = mapped_column(
        ForeignKey("variantes.id"), nullable=False
    )
    deposito_id: Mapped[int] = mapped_column(
        ForeignKey("depositos.id"), nullable=False
    )
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    tipo_movimiento: Mapped[str] = mapped_column(String(30), nullable=False)
    estado_origen: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    estado_destino: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    referencia_tipo: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    referencia_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class PedidoCliente(Base):
    """Pedido de un cliente cuando no hay stock disponible (backorder).
    No genera movimiento de inventario porque no hay pieza fisica
    todavia: cuando llega la mercaderia y se concreta la venta, ahi si
    se generan los movimientos reales (compra -> venta) y este registro
    se marca como cumplido.
    """

    __tablename__ = "pedidos_cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("clientes.id"), nullable=True
    )
    variante_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("variantes.id"), nullable=True
    )
    descripcion_libre: Mapped[Optional[str]] = mapped_column(
        String(250), nullable=True
    )
    cantidad: Mapped[int] = mapped_column(default=1, nullable=False)
    fecha_pedido: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[str] = mapped_column(
        String(20), default="pendiente", nullable=False
    )
    venta_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("ventas.id"), nullable=True
    )
