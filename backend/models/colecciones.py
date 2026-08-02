"""Colecciones estilo moda y su relacion N a N con articulos.

Una coleccion incluye N articulos y un articulo puede pertenecer a N
colecciones (por ejemplo un mismo anillo puede estar en la coleccion de
verano y en una edicion limitada al mismo tiempo).
"""

from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Column, Date, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base

coleccion_articulos = Table(
    "coleccion_articulos",
    Base.metadata,
    Column("coleccion_id", ForeignKey("colecciones.id"), primary_key=True),
    Column("articulo_id", ForeignKey("articulos.id"), primary_key=True),
)


class Coleccion(Base):
    __tablename__ = "colecciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    fecha_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    activa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # backref "colecciones" queda disponible del lado de Articulo sin
    # tener que tocar el modelo de catalogo.py
    articulos = relationship(
        "Articulo", secondary=coleccion_articulos, backref="colecciones"
    )
