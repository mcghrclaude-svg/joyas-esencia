"""Fixture de base de datos de test. Importa explicitamente todos los
modulos de backend/models/ antes de create_all() (ADR-006): si un
modelo nuevo no se importa aca, SQLAlchemy no ve su tabla y los tests
fallan de forma confusa.

Al agregar un modelo nuevo en backend/models/, sumar su import en la
lista de abajo.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models.base import Base

# Import explicito de todos los modulos de modelos (ADR-006).
from backend.models import catalogo  # noqa: F401
from backend.models import colecciones  # noqa: F401
from backend.models import combos  # noqa: F401
from backend.models import compras  # noqa: F401
from backend.models import inventario  # noqa: F401
from backend.models import precios  # noqa: F401
from backend.models import proveedores  # noqa: F401
from backend.models import usuarios  # noqa: F401
from backend.models import ventas  # noqa: F401


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = session_local()
    try:
        yield session
    finally:
        session.close()
