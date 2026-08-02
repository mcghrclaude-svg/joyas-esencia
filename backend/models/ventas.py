"""Clientes, ventas y detalle de venta. venta_items vende una variante
suelta o un combo (exactamente uno de los dos FK debe estar seteado).
"""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class Cliente(Base):
    """Datos minimos de cliente, pensados para armar base de mailing a
    futuro (acepta_mailing filtra la base).
    """

    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    acepta_mailing: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    fecha_alta: Mapped[date] = mapped_column(
        Date, server_default=func.now(), nullable=False
    )


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("clientes.id"), nullable=True
    )
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    fecha: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    observaciones: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)

    items: Mapped[list["VentaItem"]] = relationship(
        "VentaItem", back_populates="venta", cascade="all, delete-orphan"
    )


class VentaItem(Base):
    """precio_unitario_venta es el precio real cobrado en esta venta
    puntual, distinto del precio de vidriera en PrecioPublicacion
    (puede diferir por negociacion, venta en combo, etc).
    """

    __tablename__ = "venta_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    venta_id: Mapped[int] = mapped_column(ForeignKey("ventas.id"), nullable=False)
    variante_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("variantes.id"), nullable=True
    )
    combo_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("combos.id"), nullable=True
    )
    cantidad: Mapped[int] = mapped_column(default=1, nullable=False)
    precio_unitario_venta: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    venta: Mapped["Venta"] = relationship("Venta", back_populates="items")
