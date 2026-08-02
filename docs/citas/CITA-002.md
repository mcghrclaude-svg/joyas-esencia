# CITA-002: web_fetch de Claude.ai sirve contenido viejo tras un push

Fecha: 2026-08-01

## Sintoma

Despues de pushear un commit que modifica un archivo del repo, la
herramienta web_fetch de Claude.ai sigue devolviendo el contenido
anterior al pushear una URL de raw.githubusercontent.com para ese
archivo. Esto se repitio en tres sesiones distintas de Claude.ai, tanto
con como sin parametros de cache-busting en la URL.

## Causa raiz

No es cache de Fastly/GitHub del lado de raw.githubusercontent.com: se
confirmo via `gh api repos/<owner>/<repo>/contents/<archivo>` que el
blob remoto ya tenia el contenido actualizado apenas despues del push
(ver diagnostico de CITA-001, mismo incidente). El contenido viejo
queda cacheado del lado de la herramienta de fetch de Claude.ai, por un
tiempo indeterminado.

## Solucion aplicada

No reintentar fetches sueltos asumiendo que el push fallo. Antes de
sospechar de un push, verificar el estado real del remoto con:

- `git log origin/main` (despues de `git fetch origin`) para confirmar
  que el commit esperado esta en origin/main.
- `gh api repos/<owner>/<repo>/contents/<archivo>` para leer el blob
  remoto en vivo (no pasa por raw.githubusercontent.com ni por la cache
  de la herramienta de fetch).

Si el chat de Claude.ai necesita el contenido actualizado de forma
inmediata (por ejemplo para seguir trabajando en la misma conversacion
justo despues de un push), la salida practica es pegar el contenido
como texto literal en el mensaje en vez de esperar a que el fetch se
actualice.

## Como reconocerlo si vuelve a pasar

Un web_fetch a una URL de raw.githubusercontent.com devuelve contenido
que no coincide con un cambio recien pusheado, pero `git log
origin/main` y `gh api repos/<owner>/<repo>/contents/<archivo>` (via
terminal, no via web_fetch) muestran que el remoto ya tiene el
contenido nuevo.
