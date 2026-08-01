# ADR - Architecture Decision Records - Joyas MCGHR

Registro de decisiones de arquitectura del proyecto. Cada ADR es
inmutable una vez aceptado; si una decision cambia, se agrega un ADR
nuevo que supera al anterior (no se edita el original salvo para marcar
el estado como "Superado por ADR-0XX").

Formato: numero, titulo, estado (Aceptado / Propuesto / Superado),
contexto, decision, consecuencias.

---

## ADR-001: Base SQLAlchemy unica

**Estado:** Aceptado

**Contexto:** Multiples modulos backend necesitan definir modelos de datos.
Si cada modulo crea su propia Base declarativa, create_all y las
relaciones entre tablas se rompen de forma silenciosa.

**Decision:** Existe una unica Base declarativa en
backend/models/base.py. Todo modelo del proyecto hereda de esa Base,
sin excepcion.

**Consecuencias:** Cualquier modulo nuevo que necesite persistencia
importa Base desde backend/models/base.py en vez de crear la suya.

---

## ADR-002: Frontend Tailwind puro, sin CSS custom

**Estado:** Aceptado

**Contexto:** Mezclar Tailwind con CSS custom (archivos .css sueltos,
CSS-in-JS, modulos .module.css) genera inconsistencia visual y dificulta
mantener un design system unico para el catalogo.

**Decision:** Todo el estilo del frontend se resuelve con clases de
Tailwind y los tokens definidos en frontend/tailwind.config.js. No se
agregan archivos .css custom mas alla del entry point minimo que
Tailwind requiere.

**Consecuencias:** Los ajustes de diseno (colores, espaciado, tipografia)
se hacen editando tailwind.config.js, no CSS suelto.

---

## ADR-003: Variables VITE_* exclusivamente en frontend/.env.local

**Estado:** Aceptado

**Contexto:** El frontend (Vite) necesita configuracion por entorno (URL
de API, claves publicas). Si estas variables se hardcodean en el codigo
o se commitean, cualquier cambio de entorno requiere tocar codigo fuente
y se arriesga a filtrar configuracion sensible.

**Decision:** Toda variable de entorno del frontend vive unicamente en
frontend/.env.local (gitignored). El codigo las lee via
import.meta.env.VITE_*. Nunca se hardcodean valores de entorno en el
codigo fuente.

**Consecuencias:** frontend/.env.local debe existir localmente en cada
maquina de desarrollo; no viaja por git. Se documenta un
frontend/.env.example (sin valores reales) cuando exista contenido real
que documentar.

---

## ADR-004: IDs de catalogo autogenerados como slug

**Estado:** Aceptado

**Contexto:** El catalogo online necesita URLs e identificadores legibles
para cada pieza (para SEO y para compartir links), no solo IDs numericos
internos.

**Decision:** Cada item de catalogo genera automaticamente un slug (a
partir del nombre/categoria) como identificador publico, separado del ID
interno de base de datos.

**Consecuencias:** El slug debe garantizarse unico antes de persistir
(colision -> sufijo numerico). El ID interno de base de datos nunca se
expone en URLs publicas.

---

## ADR-005: Modulos nuevos en frontend/src/modules/, nunca en pages/

**Estado:** Aceptado

**Contexto:** Mezclar logica de modulo de negocio (componentes, hooks,
estado) directamente en la carpeta de paginas/rutas hace que crezcan
archivos gigantes y dificulta reutilizar logica entre vistas.

**Decision:** Toda funcionalidad nueva (por ejemplo: inventario, catalogo,
clientes) se organiza como un modulo autocontenido en
frontend/src/modules/<nombre-modulo>/. Las paginas/rutas solo componen e
importan desde modules/, no contienen logica de negocio propia.

**Consecuencias:** Antes de agregar una feature hay que decidir a que
modulo pertenece o crear uno nuevo; no se agrega logica de negocio suelta
en pages/.

---

## ADR-006: conftest.py importa todos los modelos explicitamente antes de create_all

**Estado:** Aceptado

**Contexto:** SQLAlchemy solo registra en su metadata los modelos que
efectivamente fueron importados en algun punto del proceso. Si los tests
llaman a Base.metadata.create_all() sin haber importado todos los
modulos de modelos, las tablas de los modelos no importados no se crean
y los tests fallan de forma confusa.

**Decision:** backend/tests/conftest.py importa explicitamente todos los
modulos de backend/models/ antes de invocar create_all() en el fixture
de base de datos de test.

**Consecuencias:** Al agregar un modelo nuevo hay que sumar su import en
conftest.py, o el test suite empieza a fallar por tablas faltantes.

---

## ADR-007: Scripts PS1 con ErrorActionPreference Continue + try/catch en git

**Estado:** Aceptado

**Contexto:** Los scripts de mantenimiento de repo (cierre de sesion,
creacion de branches, chequeo de conflictos) corren comandos git que
pueden fallar por razones esperables (branch ya existe, no hay cambios
para commitear, etc.). Si $ErrorActionPreference = 'Stop' o si no se
capturan los errores de git, el script corta la ejecucion en el primer
comando no criticov y deja al usuario sin diagnostico claro.

**Decision:** Todo script .ps1 de scripts/ setea
$ErrorActionPreference = 'Continue' y envuelve cada comando git en un
bloque try/catch que reporta el error sin abortar el script completo.
Ademas, cualquier resultado de Get-ChildItem que luego se use con
.Count se envuelve en @() para evitar el error de PowerShell cuando el
resultado es un unico objeto o esta vacio.

**Consecuencias:** Los scripts son mas verbosos (mas try/catch) a cambio
de ser robustos ante fallos parciales esperables.

---

## ADR-008: Chats paralelos usan branches por tema, validadas antes de mergear a main

**Estado:** Aceptado

**Contexto:** Varios chats de Claude.ai/Claude Code pueden trabajar en
paralelo sobre temas distintos del mismo repo (por ejemplo: modulo de
inventario vs. modulo de catalogo). Si todos escriben directo sobre
main, los cambios se pisan entre si sin posibilidad de revision.

**Decision:** Cada tema de trabajo en paralelo usa su propia branch
(convencion: feature/<tema-slug>). Antes de mergear a main se valida
que no haya conflictos (ver scripts/chequear-conflictos.ps1) y que el
tema este efectivamente cerrado.

**Consecuencias:** main se mantiene siempre en estado desplegable. La
creacion de branches por tema se apoya en
scripts/iniciar-chat-tema.ps1.

---

## ADR-009: [PLACEHOLDER] Gobierno de automatizacion futura via Claude Desktop

**Estado:** Propuesto (placeholder, no completar hasta que exista
necesidad real)

**Contexto:** A futuro puede existir la necesidad de que Claude Desktop
automatice tareas recurrentes sobre este proyecto (por ejemplo:
importacion de fotos de producto, generacion automatica del catalogo en
PDF, sincronizacion con una plataforma de e-commerce). Este tipo de
automatizacion no debe empezar a existir por iniciativa propia del
agente.

**Decision:** Este ADR se completa recien cuando Hernan defina
explicitamente en Claude.ai una necesidad real de automatizacion,
siguiendo el mismo patron de gobierno usado en ADR-001/ADR-003 de
Finanzas MCGHR. Hasta entonces, el rol de automatizacion de Claude
Desktop para este proyecto queda en pausa.

**Consecuencias:** Ninguna automatizacion programada (tareas
recurrentes, ETL, sincronizaciones) se implementa sin que este ADR se
complete primero.
