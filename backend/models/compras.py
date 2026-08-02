"""Compras a proveedores. compra_items registra cantidad y costo por
lote (variante + compra): no se distinguen unidades individuales
dentro de un mismo lote, ej. 5 anillos iguales comprados juntos son
una sola fila con cantidad=5.
"""

from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class Compra(Base):
    """Cabecera de una compra. precio_gramo_compra es el valor fijo e
    historico del gramo al momento de esta compra puntual (nunca se
    actualiza despues); se compara contra PrecioGramo vigente para
    calcular el % de variacion de costo de reposicion.
    """

    __tablename__ = "compras"

    id: Mapped[int] = mapped_column(primary_key=True)
    proveedor_id: Mapped[int] = mapped_column(
        ForeignKey("proveedores.id"), nullable=False
    )
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materiales.id"), nullable=False
    )
    fecha_compra: Mapped[date] = mapped_column(Date, nullable=False)
    numero_factura: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    precio_gramo_compra: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    items: Mapped[list["CompraItem"]] = relationship(
        "CompraItem", back_populates="compra", cascade="all, delete-orphan"
    )


class CompraItem(Base):
    """Cantidad y costo unitario de una variante dentro de una compra."""

    __tablename__ = "compra_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    compra_id: Mapped[int] = mapped_column(ForeignKey("compras.id"), nullable=False)
    variante_id: Mapped[int] = mapped_column(
        ForeignKey("variantes.id"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(nullable=False)
    costo_unitario_compra: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    compra: Mapped["Compra"] = relationship("Compra", back_populates="items")
