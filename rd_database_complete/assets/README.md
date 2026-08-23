# Flujo de iconos CHEMSEX

Guía de trabajo para generar, limpiar y guardar los iconos del carrusel CHEMSEX. Se creó después de corregir varias iteraciones de los iconos de las láminas 5, 6 y 7.

## Fuentes de verdad

- Repositorio: `C:\IA\svg`.
- Texto y orden de las láminas: `agent-toolkit/projects/chemsex/storyboard.json`.
- Base editorial RD: `rd_database_complete/rd_complete.db`.
- Assets canónicos: `rd_database_complete/assets/`.
- Referencias de estilo sobrio: `slide6_care_icons_sober_v1/` y `slide7_interactions_icons_sober_v1/`.

Antes de generar un icono, revisar el storyboard y comparar visualmente con los assets canónicos. No asumir que una carpeta o una imagen generada corresponde a la versión final.

## Estilo aprobado

- Paleta sobria: azul marino profundo, azul/teal apagado, verde oliva, crema y terracota moderado.
- Contornos oscuros gruesos, formas planas y composición compacta.
- Textura de serigrafía/risografía limpia y moderada.
- Sin texto, logos, marcas de agua, sombras proyectadas, halos ni fondos decorativos.
- Evitar la microtrama densa: no deben quedar puntitos blancos aislados ni ruido blanco dentro de las formas.

## Flujo correcto

1. Generar o editar con la herramienta integrada `image_gen`.
2. Para editar un archivo local, inspeccionarlo primero con `view_image`.
3. Pedir explícitamente `actual transparent alpha`, sin damero, backplate blanco/gris ni píxeles blancos fuera de las formas.
4. Si el generador entrega textura sucia, editar el PNG generado preservando la composición y pedir colores planos con pocas manchas de textura amplia.
5. Revisar visualmente el resultado sobre el fondo negro del visor y sobre un fondo contrastante.
6. Solo después copiar el archivo a la carpeta canónica de la lámina.

## Fondo transparente: reglas críticas

- El damero visible dentro del PNG significa que el fondo está incrustado; no es transparencia real.
- Un píxel de esquina transparente no basta como validación. Revisar todos los bordes.
- La extracción debe conservar los tonos crema, los highlights y el antialiasing de los contornos.
- No aplicar un umbral global de colores neutros sobre toda la imagen después de generar el icono: puede borrar áreas crema y tramas internas.
- No eliminar todos los componentes claros pequeños dentro del dibujo: algunos pertenecen a la ilustración.
- No ejecutar una segunda limpieza de componentes sin copiar primero todos los píxeles no eliminados; una rutina defectuosa puede dejar el PNG completamente vacío.
- Si es necesario recortar un damero incrustado, eliminar únicamente el fondo conectado al borde o usar la edición de `image_gen` para preservar la ilustración. Revisar siempre el resultado antes de reemplazar el asset.

El umbral histórico usado en una iteración anterior fue `max(R,G,B)-min(R,G,B) <= 16` y `promedio >= 208`. Es solo una referencia de compatibilidad; no usarlo automáticamente sobre un icono con colores claros internos.

## Validación mínima antes de guardar

Para cada PNG final:

- Modo RGBA.
- Esquina `(0,0)` con alpha `0`.
- `edgeOpaque = 0` en los cuatro bordes.
- Sin damero visible en huecos internos.
- Sin píxeles blancos aislados o microtrama aleatoria.
- Antialiasing conservado en los bordes, como en los iconos de las láminas 6 y 7.
- Comparación visual con al menos un asset canónico de `slide6_care_icons_sober_v1/`.

## Guardado y Git

- Usar nombres descriptivos y estables, por ejemplo `04_salud_mental_comedown_autolesion_dependencia.png`.
- Guardar el PNG dentro de la carpeta de la lámina correspondiente.
- Hacer `git add` solo sobre el archivo o carpeta trabajada; el repositorio contiene otros archivos no relacionados.
- Revisar `git diff --cached --stat` antes del commit.
- Después del push, confirmar que `git rev-parse HEAD` coincide con `git ls-remote origin refs/heads/main`.

## Errores que ya ocurrieron y no repetir

- Confundir el fondo negro del visor con un fondo negro real: el visor muestra la transparencia sobre negro.
- Aceptar una imagen con damero incrustado porque la esquina parecía limpia.
- Usar una limpieza global que perforó las zonas claras del dibujo.
- Usar una limpieza de componentes que eliminó el contenido del PNG.
- Reemplazar el asset canónico antes de inspeccionar visualmente la versión procesada.

