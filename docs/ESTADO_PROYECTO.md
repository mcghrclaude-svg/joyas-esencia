# ESTADO DEL PROYECTO - Joyas MCGHR

Ultima actualizacion: 2026-08-01 (fix de gobierno: URLs para web_fetch)

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
- Esqueleto frontend (sin logica): frontend/src/modules/ vacio,
  frontend/tailwind.config.js con tokens placeholder.
- .gitignore cubriendo entornos, datos de negocio y salidas generadas.

## Falta / no arrancado todavia

- Todo el modelado de datos real (productos, stock, categorias,
  clientes).
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
