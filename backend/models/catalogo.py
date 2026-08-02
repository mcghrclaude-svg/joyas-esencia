"""Modelos del catalogo maestro: categorias, materiales, articulos,
variantes y fotos. Ver ADR-001 (Base unica) y ADR-004 (slug) en
docs/ADR.md.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base


class Categoria(Base):
    """Categoria jerarquica de tipo de joya (anillo, anillo/grande, etc).

    La jerarquia se modela con auto-referencia. Este modelo deja
    preparada la estructura; la carga real del arbol de categorias se
    hace desde la pantalla de administracion.
    """

    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    categoria_padre_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categorias.id"), nullable=True
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    categoria_padre: Mapped[Optional["Categoria"]] = relationship(
        "Categoria", remote_side=[id], back_populates="subcategorias"
    )
    subcategorias: Mapped[list["Categoria"]] = relationship(
        "Categoria", back_populates="categoria_padre"
    )


class Material(Base):
    """Material estructurado (oro 18k, plata 925, etc), administrable
    desde la pantalla de mantenimiento de maestros.

    El precio del gramo NO vive aca: ver PrecioGramo en precios.py, que
    es una relacion 1 a N por fecha (el precio cambia en el tiempo).
    """

    __tablename__ = "materiales"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    tipo_metal: Mapped[str] = mapped_column(String(40), nullable=False)
    ley_pureza: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Articulo(Base):
    """Maestro de articulos (SKU). Representa el diseno/producto, no el
    stock fisico: el stock vive en Variante + MovimientoInventario.
    """

    __tablename__ = "articulos"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    descripcion_interna: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    descripcion_publica: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    categoria_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categorias.id"), nullable=True
    )
    material_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("materiales.id"), nullable=True
    )
    peso_referencia_gr: Mapped[Optional[float]] = mapped_column(nullable=True)
    estado_publicacion: Mapped[str] = mapped_column(
        String(20), default="borrador", nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    fecha_alta: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    categoria: Mapped[Optional["Categoria"]] = relationship("Categoria")
    material: Mapped[Optional["Material"]] = relationship("Material")
    variantes: Mapped[list["Variante"]] = relationship(
        "Variante", back_populates="articulo", cascade="all, delete-orphan"
    )
    fotos: Mapped[list["ArticuloFoto"]] = relationship(
        "ArticuloFoto", back_populates="articulo", cascade="all, delete-orphan"
    )


class Variante(Base):
    """Variante vendible de un articulo (por talla, por ejemplo).

    Todo articulo tiene al menos una variante, incluso si no hay
    variacion real (variante unica sin talla). El resto del sistema
    (compras, stock, ventas, precios) siempre referencia una variante,
    nunca el articulo directamente. Esto evita tener dos caminos
    distintos en el codigo segun si el articulo tiene variantes o no.
    """

    __tablename__ = "variantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    articulo_id: Mapped[int] = mapped_column(
        ForeignKey("articulos.id"), nullable=False
    )
    sku_variante: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    talla: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    articulo: Mapped["Articulo"] = relationship("Articulo", back_populates="variantes")


class ArticuloFoto(Base):
    """Foto de galeria de un articulo (una puede marcarse como
    principal). Se guarda ruta relativa al filesystem del servidor,
    nunca una ruta absoluta de perfil de usuario de Windows especifico
    (ver CLAUDE.md). Un articulo puede no tener ninguna foto todavia.
    """

    __tablename__ = "articulo_fotos"

    id: Mapped[int] = mapped_column(primary_key=True)
    articulo_id: Mapped[int] = mapped_column(
        ForeignKey("articulos.id"), nullable=False
    )
    ruta_relativa: Mapped[str] = mapped_column(String(255), nullable=False)
    es_principal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    orden: Mapped[int] = mapped_column(default=0, nullable=False)

    articulo: Mapped["Articulo"] = relationship("Articulo", back_populates="fotos")
