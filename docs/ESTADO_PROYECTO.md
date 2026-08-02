# ESTADO DEL PROYECTO - Joyas MCGHR

Ultima actualizacion: 2026-08-01 (modelos SQLAlchemy y vista de stock)

## Resumen

Proyecto recien inicializado. Existe la estructura de gobierno
(documentacion, ADRs, scripts de mantenimiento de repo) y un esqueleto
vacio de backend/frontend, sin logica de negocio todavia.

## Hecho

- Repo publico creado: mcghrclaude-svg/joyas-esencia
- Estructura de documentacion: CLAUDE.md, docs/ADR.md, docs/CITA.md,
  docs/citas/, docs/HANDOFF_20260801.md, este archivo.
- Scripts de mantenimiento de repo: scripts/cerrar-sesion.ps1,
  scripts/iniciar-chat-tema.ps1, scripts/chequear-conflictos.ps1.
- Fix de gobierno: seccion "URLs para web_fetch" en CLAUDE.md con el
  indice literal de URLs raw.githubusercontent.com de docs/ADR.md,
  docs/CITA.md, docs/ESTADO_PROYECTO.md y el HANDOFF_*.md mas reciente.
  Se agrego docs/citas/CITA-001.md documentando que api.github.com esta
  bloqueada por deteccion de bots para la herramienta web_fetch de
  Claude.ai (usar siempre raw.githubusercontent.com, nunca
  api.github.com, para leer archivos de este repo desde Claude.ai).
  scripts/cerrar-sesion.ps1 ahora regenera esa seccion en cada cierre de
  sesion, recalculando el HANDOFF mas reciente por fecha de archivo.
- Esqueleto backend (sin logica): backend/models/base.py con la Base
  declarativa unica, backend/core/database.py con engine/sesion.
- Modelos SQLAlchemy de datos reales: backend/models/catalogo.py,
  colecciones.py, precios.py, combos.py, proveedores.py, compras.py,
  inventario.py, ventas.py y usuarios.py, todos sobre la Base unica de
  backend/models/base.py (ADR-001).
- Vista SQL vista_stock_actual en backend/models/views.sql.
- Paquete backend/ resuelto como paquete Python regular:
  __init__.py en backend/, backend/models/, backend/core/ y
  backend/tests/, mas pyproject.toml en la raiz con
  [tool.pytest.ini_options] pythonpath = ["."] (ADR-010).
- Esqueleto frontend (sin logica): frontend/src/modules/ vacio,
  frontend/tailwind.config.js con tokens placeholder.
- .gitignore cubriendo entornos, datos de negocio y salidas generadas.

## Falta / no arrancado todavia

- Tests de los modelos nuevos: backend/tests/conftest.py existe con el
  fixture db_session (crea las tablas en sqlite en memoria), pero
  todavia no hay ningun test_*.py que lo use. Los 9 modelos y la vista
  estan sin cobertura de tests por ahora.
- Todo el modelado de datos real (productos, stock, categorias,
  clientes) mas alla de lo ya cargado arriba.
- Toda la logica de negocio de backend (API, endpoints).
- Todo el frontend funcional (modulos reales dentro de
  frontend/src/modules/).
- Generacion de catalogo (PDF y/o web).
- Cualquier automatizacion recurrente (ver ADR-009, placeholder hasta
  que exista una decision explicita).
- Integracion con plataforma de e-commerce (futuro, sin decision
  tomada).

## Decisiones abiertas / a confirmar con Hernan

- Alcance exacto del modelo de datos de inventario (que atributos tiene
  una pieza de joyeria: material, quilates, peso, proveedor, etc.).
- Formato final del catalogo online (sitio propio vs. integracion con
  plataforma existente).
- Si el PDF de catalogo se genera on-demand o como proceso batch.

## Notas operativas

- El MCP de GitHub configurado en esta maquina no tiene permiso para
  crear repositorios (token sin ese scope). Usar `gh repo create` via
  terminal para esa operacion puntual; el resto de operaciones de git
  (push, commit, branches) funcionan normalmente.
