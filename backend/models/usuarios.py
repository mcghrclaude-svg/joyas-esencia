"""Usuarios simples: login por icono + codigo de acceso, sin roles por
ahora (todos los usuarios pueden hacer todo). codigo_hash nunca guarda
el codigo en texto plano.
"""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    icono_path: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
