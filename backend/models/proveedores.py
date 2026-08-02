"""Proveedores: entidad propia con datos de contacto, administrable
desde la pantalla de mantenimiento de maestros.
"""

from typing import Optional

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class Proveedor(Base):
    __tablename__ = "proveedores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    contacto_persona: Mapped[Optional[str]] = mapped_column(
        String(120), nullable=True
    )
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
