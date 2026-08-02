"""Historial de precios: publicacion (catalogo) y cotizacion de gramo
por material. Ambas tablas son de vigencia por fecha, nunca se pisa un
valor anterior encima de otro (trazabilidad obligatoria).
"""

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class PrecioPublicacion(Base):
    """Precio mostrado en el catalogo publico para una variante o un
    combo (exactamente uno de los dos FK debe estar seteado, nunca
    ambos ni ninguno). Es el precio "de vidriera", distinto del precio
    real cobrado en una venta (ver VentaItem.precio_unitario_venta).

    tipo distingue: normal / descuento_temporal / campana.
    """

    __tablename__ = "precios_publicacion"

    id: Mapped[int] = mapped_column(primary_key=True)
    variante_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("variantes.id"), nullable=True
    )
    combo_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("combos.id"), nullable=True
    )
    precio: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), default="normal", nullable=False)
    vigente_desde: Mapped[date] = mapped_column(Date, nullable=False)
    vigente_hasta: Mapped[Optional[date]] = mapped_column(Date, nullable=True)


class PrecioGramo(Base):
    """Cotizacion del gramo por material a lo largo del tiempo.
    Relacion 1 a N: cada material (oro, plata, plata 925, etc) tiene
    muchas cotizaciones historicas, nunca un unico valor fijo.

    Carga manual por ahora (ver ADR-009 placeholder si a futuro se
    automatiza con una fuente externa de cotizacion).
    """

    __tablename__ = "precios_gramo"

    id: Mapped[int] = mapped_column(primary_key=True)
    material_id: Mapped[int] = mapped_column(
        ForeignKey("materiales.id"), nullable=False
    )
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    precio_gramo: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
