# svg — herramientas para crear imágenes y SVG sin depender de un PC

Repositorio de trabajo de **RD / ligereza** para conservar herramientas, librerías, scripts, bases de datos y assets reutilizables desde un entorno remoto.

## Qué contiene

- `agent-toolkit/`: adaptadores, herramientas y proyectos para rasterizar, vectorizar, animar y trabajar con imágenes/SVG.
- `rd_database_complete/`: base de datos y bibliotecas de iconos para reducción de daños, incluyendo los iconos generados en PNG y su conversión vectorial en `assets/generated_icons/svg/`.
- `umbrella/`, `three.js/`, `d3/`, `rxjs/`, `effect/`, `stdlib/`, `d3-test/`: fuentes de librerías útiles para gráficos, SVG, geometría, animación y procesamiento.
- `chemsex_*.png`, `*.svg`, `*.py` y `HANDOFF_*.md`: composiciones, exportaciones y scripts del flujo Chemsex.
- `remote_imports/`, `review_renders/` y `cover-review/`: materiales importados y revisiones que siguen siendo reutilizables.

## Iconos generados

Los 48 iconos generados se conservan en dos formatos:

- PNG original: `rd_database_complete/assets/generated_icons/*.png`
- SVG vectorizado: `rd_database_complete/assets/generated_icons/svg/*.svg`

La conversión se realizó con `agent-toolkit/adapters/image/vectorize.py` usando trazados SVG reales. Los SVG son una vectorización rasterizada a resolución reducida; no se presentan como estructuras químicas ni como identificación analítica de una sustancia.

## Exclusiones intencionales

No se versionan instalaciones locales (`node_modules`), cachés, temporales, metadatos Git anidados ni credenciales. Las dependencias se pueden reinstalar desde los manifiestos de cada librería.
