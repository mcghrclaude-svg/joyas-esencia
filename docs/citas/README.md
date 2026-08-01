# docs/citas/ - Criterio de creacion

Esta carpeta guarda fichas CITA-0XX.md, una por cada error real que fue
diagnosticado y resuelto en el proyecto (bugs de codigo, problemas de
configuracion, fallas de infraestructura, etc.).

## Cuando SI crear una CITA-0XX.md

- El error ocurrio de verdad (no es una hipotesis ni un riesgo teorico).
- Ya se identifico la causa raiz.
- Ya se aplico y verifico una solucion.

## Cuando NO crear una

- Como documentacion preventiva de algo que "podria pasar".
- Como nota de diseno o decision de arquitectura (eso va en
  [docs/ADR.md](../ADR.md)).
- Como TODO o tarea pendiente (eso va en
  [docs/ESTADO_PROYECTO.md](../ESTADO_PROYECTO.md)).

## Formato sugerido de cada CITA-0XX.md

```
# CITA-0XX: Titulo corto del error

Fecha: YYYY-MM-DD

## Sintoma
Que se observaba.

## Causa raiz
Que lo provocaba realmente.

## Solucion aplicada
Que se cambio para resolverlo.

## Como reconocerlo si vuelve a pasar
Senales o mensajes de error especificos a buscar.
```

Cada CITA-0XX.md nueva se suma como fila en [docs/CITA.md](../CITA.md).
