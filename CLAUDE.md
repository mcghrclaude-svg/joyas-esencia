# CLAUDE.md - Joyas MCGHR

Este archivo guia a cualquier instancia de Claude (Claude.ai, Claude Code,
Claude Desktop) que trabaje en este repositorio.

## Que es este proyecto

Joyas MCGHR es un sistema de gestion de inventario de joyas para venta y
publicacion en catalogo online. Cubre carga de productos, control de stock,
generacion de catalogo (PDF y/o web) y, a futuro, publicacion en una
plataforma de e-commerce.

## Roles de trabajo

- **Hernan** es el desarrollador. En Claude.ai actua como supervisor/apoyo
  tecnico: disena, decide y genera contenido (codigo, specs, ADRs) que luego
  se materializa en este repo.
- **Claude Desktop / Claude Code** (la instancia que lee este archivo) es el
  motor de ejecucion: ejecuta comandos de filesystem y git directamente.
  Su rol de automatizacion queda en pausa fuera del bootstrap inicial hasta
  que exista una necesidad real respaldada por un ADR (ver docs/ADR.md).
- Los chats paralelos sobre temas distintos trabajan en branches propias,
  nunca directo sobre main. Ver ADR-008 y scripts/iniciar-chat-tema.ps1.

## Reglas de codigo (obligatorias)

- Solo ASCII en codigo, comentarios, nombres de archivo y mensajes de
  commit. Nunca acentos ni enie.
- Nunca hardcodear rutas absolutas de un perfil de usuario de Windows
  especifico (ej. C:\Users\alguien\...) en codigo o configuracion de la
  aplicacion. El usuario final corre la app con una cuenta de Windows
  distinta a la del desarrollador. Las rutas de datos (DB, uploads, PDFs)
  van relativas al repo o por variable de entorno.
- No commitear datos sensibles del negocio (costos, margenes, datos de
  clientes) a este repo, que es publico.
- Base SQLAlchemy unica en backend/models/base.py (ADR-001).
- Frontend Tailwind puro, sin CSS custom (ADR-002).
- Variables VITE_* exclusivamente en frontend/.env.local, nunca commiteado
  (ADR-003).
- IDs de catalogo autogenerados como slug (ADR-004).
- Modulos nuevos de frontend van en frontend/src/modules/, nunca en
  pages/ (ADR-005).
- conftest.py debe importar todos los modelos explicitamente antes de
  llamar a create_all (ADR-006).
- Scripts .ps1 usan $PSScriptRoot, reciben la ruta del repo como parametro
  (nunca hardcodeada), documentan el bypass de ExecutionPolicy en un
  comentario de cabecera, envuelven cualquier Get-ChildItem con @() antes
  de usar .Count, y usan $ErrorActionPreference = 'Continue' con
  try/catch alrededor de los comandos git (ADR-007).

## Estructura de carpetas

```
Joyas_Esencia/
  CLAUDE.md
  docs/
    ADR.md              - decisiones de arquitectura
    CITA.md             - indice de citas de errores resueltos
    citas/              - CITA-0XX.md individuales
    HANDOFF_*.md        - traspaso de sesion por fecha
    ESTADO_PROYECTO.md  - estado actual, se actualiza en cada commit de cierre
  scripts/
    cerrar-sesion.ps1
    iniciar-chat-tema.ps1
    chequear-conflictos.ps1
  backend/
    models/base.py
    core/database.py
  frontend/
    src/modules/
    tailwind.config.js
```

## Documentos que hay que leer antes de tocar codigo

1. [docs/ADR.md](docs/ADR.md) - decisiones ya tomadas, no las repitas ni las
   contradigas sin ADR nuevo.
2. [docs/ESTADO_PROYECTO.md](docs/ESTADO_PROYECTO.md) - que esta hecho y que
   falta.
3. [docs/CITA.md](docs/CITA.md) - errores ya resueltos, revisar antes de
   depurar algo que huele a ya-visto.
4. El HANDOFF_*.md mas reciente en docs/ - contexto de la ultima sesion.

## URLs para web_fetch

<!-- INICIO-AUTOGENERADO: URLs para web_fetch, no editar a mano, ver scripts/cerrar-sesion.ps1 -->
Estas URLs raw sirven para que Claude.ai (via web_fetch) lea el estado
real del repo sin depender de contenido de sesiones anteriores. Nunca
usar api.github.com para esto (ver docs/citas/CITA-001.md): esta
bloqueada por deteccion de bots para la herramienta web_fetch.

- https://raw.githubusercontent.com/mcghrclaude-svg/joyas-esencia/main/docs/ADR.md
- https://raw.githubusercontent.com/mcghrclaude-svg/joyas-esencia/main/docs/CITA.md
- https://raw.githubusercontent.com/mcghrclaude-svg/joyas-esencia/main/docs/ESTADO_PROYECTO.md
- https://raw.githubusercontent.com/mcghrclaude-svg/joyas-esencia/main/docs/HANDOFF_20260801.md

Esta lista se regenera automaticamente en cada cierre de sesion (ver
scripts/cerrar-sesion.ps1); el HANDOFF listado es siempre el mas
reciente segun fecha de archivo.
<!-- FIN-AUTOGENERADO -->

## Cierre de sesion

Toda tarea que se cierra debe actualizar docs/ESTADO_PROYECTO.md en el
mismo commit, nunca como paso separado. Usar scripts/cerrar-sesion.ps1 como
apoyo para verificar el estado del repo antes de cerrar.
