"""Combos: agrupan variantes existentes con un precio propio de venta
combinada. Un combo NO genera un SKU fisico nuevo ni stock propio: el
stock sigue viviendo en las variantes componentes (ver combo_items).
Esto permite tener publicado el combo y los articulos sueltos al mismo
tiempo sin duplicar inventario.
"""

from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class Combo(Base):
    __tablename__ = "combos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    vigente_desde: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    vigente_hasta: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    items: Mapped[list["ComboItem"]] = relationship(
        "ComboItem", back_populates="combo", cascade="all, delete-orphan"
    )


class ComboItem(Base):
    """Variante y cantidad que componen un combo. Al vender un combo,
    el movimiento de inventario descuenta cada variante componente
    segun la cantidad definida aca.
    """

    __tablename__ = "combo_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    combo_id: Mapped[int] = mapped_column(ForeignKey("combos.id"), nullable=False)
    variante_id: Mapped[int] = mapped_column(
        ForeignKey("variantes.id"), nullable=False
    )
    cantidad: Mapped[int] = mapped_column(default=1, nullable=False)

    combo: Mapped["Combo"] = relationship("Combo", back_populates="items")
