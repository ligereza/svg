# Bibliotecas completas para el carrusel Chemsex

Estas carpetas son las fuentes completas descargadas. No son una selección de íconos sueltos.

## Bioicons

- Repositorio: https://github.com/duerrsimon/bioicons
- Carpeta local: `bioicons/`
- Commit descargado: `d29e766`
- Contenido: 2.836 SVG en el repositorio; 2.830 SVG de íconos organizados por carpeta de licencia y 6 SVG de interfaz del sitio.
- Distribución de los íconos SVG: CC0 488, CC BY 3.0 1.376, CC BY 4.0 885, CC BY-SA 3.0 4, CC BY-SA 4.0 35, BSD 3 y MIT 39.
- Uso en Chemsex: drogas genéricas, tabletas, cápsulas, botellas, jeringa, gotas, cerebro, corazón, pulmones, hígado, sangre, toxicidad y símbolos científicos.
- Regla de licencia: la licencia se toma del directorio de cada ícono; no se debe asumir que todo Bioicons es CC0.

## Health Icons

- Repositorio: https://github.com/resolvetosavelives/healthicons
- Carpeta local: `healthicons/`
- Commit descargado: `36887b2`
- Contenido: 2.080 SVG de íconos, 6.133 PNG y 1 JPG; los SVG están en estilos `filled`, `outline`, `filled-24px` y `outline-24px`.
- Licencia declarada para los íconos: dominio público CC0. El repositorio también contiene código del sitio con licencia MIT; esa licencia no cambia la licencia declarada de los íconos.
- Uso en Chemsex: cannabis, pastillas, jeringas, botellas médicas, preservativos, agua, sangre, corazón, pulmones, hígado, virus, salud mental, personas, emergencia y prevención.

## SVG Repo: colección temática pendiente

- Colección localizada: https://www.svgrepo.com/vectors/drug-addiction/
- La página anuncia 48 vectores sobre adicción y muestra referencias a GHB, ecstasy, joint, pills, injection y otros símbolos.
- Estado real: no se incorporó como biblioteca local porque el sitio devolvió un checkpoint de Vercel y respuestas HTTP 429 al intentar la descarga automatizada en bloque.
- No cuento esos 48 vectores como descargados. El único SVGRepo que ya existía en el proyecto es el asset individual `assets/svgrepo-drug-9406.svg`.

## Lote inicial indexado

El lote está en `chemsex-library-candidates.json`. Contiene rutas locales de referencia, no copias duplicadas. La siguiente etapa es previsualizar y validar estas rutas con las herramientas del `agent-toolkit`, y solo después copiar al carrusel los SVG elegidos.

## Criterio de trabajo

1. Buscar dentro de las bibliotecas completas por categorías y nombres relacionados.
2. Previsualizar en lote.
3. Validar SVG y revisar licencia a nivel de archivo.
4. Rasterizar únicamente cuando haga falta una imagen PNG.
5. Incorporar al carrusel solo los assets aprobados, conservando la atribución o nota CC0 correspondiente.
