# Base de datos completa RD

Construida el 18 de agosto de 2026 desde las fuentes recuperadas localmente y las dos bases copiadas desde Mak. Las fuentes originales no se modificaron.

## Archivos principales

- `rd_complete.db`: SQLite canónica ampliada.
- `build_rd_complete_database.py`: constructor reproducible.
- `rd_drug_correlation.html`: explorador focalizado en drogas, imágenes, reactivos, colorimetría y testeos 2025.
- `build_rd_drug_correlation.py`: constructor reproducible de la capa de correlación.
- `README.md`: este inventario y guía de uso.

Reconstrucción:

```powershell
$py='C:\Users\issvk\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $py 'C:\IA\svg\rd_database_complete\build_rd_complete_database.py' --force
```

## Capas incluidas

1. **Catálogo canónico de Mak**: las 20 tablas heredadas se conservan en el mismo archivo, con sus filas originales.
2. **Universo semántico RD**: 48 entidades, 50 alias, 48 fichas, 52 relaciones y 102 evidencias de relaciones.
3. **Fuentes y trazabilidad**: 74 fuentes catalogadas, manifiesto de 21.306 archivos recuperados y 44 artefactos RD preservados como texto o BLOB.
4. **Reactivos y límites**: 12 reactivos normalizados, 60 reacciones, 36 limitaciones y las correcciones de auditoría internacional.
5. **Testeos**: 42 hojas/eventos, 1.831 filas fuente, 1.646 filas de datos y 5.394 observaciones, además de mapas de sustancias/reactivos y 84 enlaces pendientes de revisión.
6. **Contenido editorial RD**: 1 post, 7 láminas, 3 claims de interacción y 7 briefs visuales, conservados como capa de contenido y no mezclados con evidencia científica.
7. **Evidencia web**: 180 páginas Firecrawl de las dos corridas recuperadas.
8. **Datos de campo**: se preserva el esquema de `rd_datos.db`; sus tres tablas estaban vacías, por lo que no se fabricaron registros.

## Capa de drogas y testeos

La capa adicional reúne 80 activos visuales y 78 vínculos visuales: 9 fotografías de kits/materiales RD, 13 fotografías reales de fuentes públicas, 48 iconos editoriales generados y 10 fotografías de reactivos. Mantiene 30 relaciones semánticas droga–reactivo, 4.783 observaciones cromáticas de filas de datos 2025 y 46 combinaciones droga–reactivo observadas en 2025.

Cada una de las 48 entidades tiene exactamente un icono editorial generado, con un motivo visual propio y un vínculo individual. Las fotografías reales se muestran primero cuando existen; el icono se usa como referencia editorial secundaria. No se utilizan estructuras químicas ni una pastilla genérica como sustituto para todas las drogas, y ningún icono se presenta como identificación química.

- Las imágenes reales son fotografías de kits o materiales publicados por RD; su licencia de reutilización quedó marcada como `source_license_unverified`.
- Las fotografías públicas descargadas y sus páginas de origen, licencia, atribución, tamaño y SHA-256 están en `public_libraries/PUBLIC_LIBRARY_MANIFEST.json`.
- Bioicons se conserva como archivo completo; la licencia debe verificarse por icono individual. Healthicons se conserva como archivo completo; sus iconos son CC0 y el repositorio incluye código MIT.
- Los iconos editoriales generados están en `assets/generated_icons/`, son PNG transparentes creados con la herramienta de generación de imágenes y se registran como `generated_internal`; no son una biblioteca científica ni una representación química.
- Las fotografías de Wikimedia Commons se registran con la licencia de cada archivo. Las imágenes CDC/PHIL incorporadas son solo las marcadas como dominio público en su ficha.
- `expected_color_*` representa la referencia de la ficha del reactivo.
- `normalized_color_*` representa una normalización heurística del texto escrito en el registro 2025.
- `observed_2025_only` significa que hubo observación, pero no existe una relación científica directa registrada; no se convierte en una afirmación de identidad.

Abrir el visor:

```text
C:\IA\svg\rd_database_complete\rd_drug_correlation.html
```

## Validación realizada

- `PRAGMA integrity_check`: `ok`.
- `PRAGMA foreign_key_check`: 0 violaciones.
- Evidencias de relaciones sin fuente catalogada: 0.
- Importación: `completed`.
- La auditoría visual confirma 48 activos `generated_icon`, 48 vínculos, 48 entidades cubiertas, 0 duplicados y 0 archivos faltantes.
- SHA-256 de `rd_complete.db`: `84162afb0aadf308bd035d89881df79ec114cdbb44ca6ead9fa33f355cb7e8ae`.

## Consultas rápidas

```sql
SELECT * FROM v_rd_entity_overview;
SELECT * FROM v_rd_relation_overview;
SELECT * FROM v_rd_test_quality;
SELECT * FROM v_rd_content_surface;
SELECT * FROM v_rd_catalog_summary;
```

Las vistas `v_rd_*` sirven para consumo rápido; las tablas `rd_*` conservan el detalle normalizado y `rd_artifact`/`rd_file_manifest` permiten volver a la fuente original.

## Límites conocidos

- Los 84 enlaces de eventos de testeo no se vincularon automáticamente a productoras o venues sin evidencia suficiente.
- Ocho entidades permanecen sin relaciones en el grafo actual; eso es una ausencia documentada, no una relación inventada.
- La base de campo recuperada contiene estructura, pero cero atenciones, encuestas y registros de testeo.
- Los archivos dentro de `.venv` se inventariaron como dependencias, pero no se interpretaron como contenido RD.
