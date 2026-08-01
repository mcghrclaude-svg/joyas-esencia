"""Base declarativa unica del proyecto. Ver ADR-001 en docs/ADR.md.

Todo modelo de backend/models/ debe heredar de esta Base, sin
excepcion, para que Base.metadata.create_all() vea todas las tablas.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
