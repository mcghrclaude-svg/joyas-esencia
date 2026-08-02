# CITA-001: api.github.com bloqueada por deteccion de bots en web_fetch

Fecha: 2026-08-01

## Sintoma

La herramienta web_fetch de Claude.ai devuelve error al intentar acceder
a endpoints de api.github.com (por ejemplo para listar el contenido de
una carpeta del repo via GitHub API, para descubrir el HANDOFF_*.md mas
reciente). El error observado es:

"CLIENT_ERROR: Site blocked the request, bot detection"

## Causa raiz

api.github.com tiene deteccion de bots que bloquea las requests hechas
por la herramienta web_fetch de Claude.ai, incluso apuntando a
endpoints publicos de un repo publico.

## Solucion aplicada

Nunca usar api.github.com para descubrir o leer archivos de este repo
desde Claude.ai. raw.githubusercontent.com si funciona sin problema
para leer el contenido de un archivo conocido. Para el caso de
descubrir que archivos existen (por ejemplo cual es el HANDOFF_*.md mas
reciente), se mantiene un indice de URLs literales en la seccion
"URLs para web_fetch" de CLAUDE.md, que se regenera en cada cierre de
sesion via scripts/cerrar-sesion.ps1.

## Como reconocerlo si vuelve a pasar

Mensaje de error de web_fetch: "CLIENT_ERROR: Site blocked the
request, bot detection" al apuntar a una URL de dominio
api.github.com.
