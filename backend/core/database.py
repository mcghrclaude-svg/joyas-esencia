"""Configuracion de engine y sesion de base de datos.

La ubicacion de la base de datos se resuelve por variable de entorno o,
si no esta seteada, relativa a la raiz del repo. Nunca hardcodear una
ruta absoluta de un perfil de usuario de Windows especifico (ver
CLAUDE.md): el usuario final corre la app con una cuenta distinta a la
del desarrollador.
"""

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = REPO_ROOT / "data" / "joyas.db"

DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
