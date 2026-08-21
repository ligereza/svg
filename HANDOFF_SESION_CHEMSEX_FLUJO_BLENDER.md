# Handoff — Carrusel Chemsex / Flujo visual Blender

**Fecha:** 2026-08-18  
**Workspace:** `C:\IA\svg`

## Objetivo inmediato

Terminar el carrusel de Chemsex para Instagram y dejar preparado un flujo reutilizable para transformar assets visuales en composiciones editables y animables dentro de Blender.

## Decisiones cerradas

- Formato final: **1080 × 1440 px, vertical**.
- El PDF `C:\Users\issvk\claude_sesiones_recuperadas\CARRUSEL CHEMSEX RevCO.pdf` contiene **solo texto**. No usarlo para evaluar portada, composición, imágenes ni estilo visual.
- El texto del PDF debe conservarse **exactamente**, sin cambiar palabras, orden ni sentido.
- La portada se trabaja con los assets visuales generados por el usuario en Firefly.
- Subtítulo de portada: **“Orgullo es cuidarnos en comunidad”**.
- No buscar más imágenes ni sustituir los assets actuales salvo solicitud explícita.
- El proyecto visual se organiza en **8 láminas**, no 10. La portada es una lámina independiente; las láminas informativas deben mantener continuidad entre conceptos relacionados.
- El lenguaje visual buscado: editorial, plano, informativo, comunitario y dinámico; minimalista sin quedar frío ni parecer una plantilla de encuesta.
- Evitar composiciones repetidas con el texto siempre en el mismo lugar. La relación entre texto, ilustración, ritmo, escala y espacio debe variar entre láminas.
- Tipografía propuesta: `Space Grotesk` para títulos y `Inter` para cuerpo, salvo que el usuario decida otra cosa.
- Blender es el núcleo del flujo visual. No volver a discutir si debe ser Illustrator o Blender.
- Usar una versión **LTS estable de Blender**; preferencia por la rama 4.5 LTS si es la instalada/compatible.
- Motor obligatorio: **Cycles**.
- Geometry Nodes es parte central del sistema para composición, repetición, distribución, animación y parametrización.
- La dirección futura es un **addon integrado** para Blender, no una colección desconectada de pequeños scripts.

## Assets actuales de portada

Archivos entregados por el usuario:

- `C:\Users\issvk\Downloads\Firefly_Gemini Flash_ADD CHEMSEX title at top area, D 830518 ZYG.png`
- `C:\Users\issvk\Downloads\Firefly_Gemini Flash_erase the heart at top, erase th 640668 V1i.png`
- `C:\Users\issvk\Downloads\Firefly_Gemini Flash_ADD CHEMSEX title at top area, D 274321 Emq.png`

Características visuales observadas:

- Fondo oscuro texturado, con dominante violeta/azul grisáceo.
- Tipografía/lettering de `CHEMSEX` con brillo, trama y colores verde, turquesa, naranja y coral.
- Dos matraces con forma de corazón en la zona inferior.
- La segunda imagen elimina el título y deja un área limpia superior.
- La tercera incorpora una grieta vertical y una lectura más dramática.
- Estos archivos son assets de trabajo; no convertirlos automáticamente en la composición final sin probar antes el recorte, escala y legibilidad del subtítulo.

## Distribución editorial vigente

La distribución trabajada hasta ahora es de 8 láminas. Mantener la lógica general y confirmar solo detalles de composición, sin volver a inventar una estructura nueva:

1. **Portada** — `CHEMSEX` + `Orgullo es cuidarnos en comunidad`.
2. **Qué es el chemsex** — definición exacta del documento; debe enlazar visualmente con la siguiente lámina.
3. **Reducción de daños / inicio del contexto** — continuidad de la lámina 2 y entrada al contexto chileno.
4. **Contexto en Chile y sustancias** — no fragmentar en demasiadas láminas; controlar la densidad con jerarquía visual e iconografía.
5. **Riesgos generales del chemsex**.
6. **Cómo cuidarnos** — usar ilustración/iconografía asociada a hidratación, no compartir material, información/testeo, PrEP/PEP/doxyPEP, cuidado mutuo y consentimiento.
7. **Interacciones más riesgosas** — puede requerir subdivisión interna o composición por módulos, pero no alterar el texto original.
8. **Cierre** — `Cuidarnos es una decisión` y el texto final del documento.

La literalidad de cada lámina debe salir del texto extraído del PDF y no de una reescritura creativa.

## Herramientas y estado conocido

- Adobe Photoshop e Illustrator están instalados y forman parte del flujo de separación, limpieza y preparación de assets.
- Adobe Firefly está disponible para generación manual con créditos del usuario.
- `PDF Services API` ya fue obtenida y está integrada en el toolkit local.
- Se configuró soporte para credenciales Adobe desde `C:\IA\flujo\.env`.
- El toolkit de trabajo está en `C:\IA\svg\agent-toolkit`.
- El procesamiento del PDF ya logró extraer texto estructurado y generar SVG por página; eso sirve para texto/estructura, no para recuperar una portada visual del PDF.
- El PDF no debe volver a tratarse como fuente de imágenes.
- La integración de Firefly API no está confirmada; no asumir que existe acceso API solo porque el usuario tiene créditos en la aplicación.

## Flujo objetivo

1. El usuario entrega el asset visual y define la lámina.
2. Photoshop separa sujeto, fondo y elementos cuando sea necesario.
3. Illustrator/SVG se usa para iconografía o ilustraciones vectoriales estáticas.
4. Blender recibe imágenes, SVG, texto y parámetros de composición.
5. Cada lámina se representa como una escena o colección editable.
6. Geometry Nodes controla distribución, repetición, conexiones, ondas, partículas, máscaras y animación.
7. Cycles produce el render final.
8. Se exportan stills 1080×1440 y, cuando corresponda, animaciones sin rasterizar prematuramente la composición completa.

## Problemas que el sistema debe resolver

- Mantener proporción y encuadre exactos de cada asset dentro de 1080×1440.
- Ubicar cada imagen en la lámina que corresponde.
- Conservar colores de SVG y evitar oscurecimiento por transparencias, solapamiento de capas o materiales incorrectos.
- Importar SVG por objetos/capas cuando sea técnicamente posible.
- Convertir selectivamente SVG a mesh o curvas sin perder editabilidad.
- Separar texto de ilustración: los recuadros son guías de composición, no la figura final.
- Medir longitud de texto, ancho disponible, tamaño de ilustración, márgenes y jerarquía con parámetros editables.
- Permitir variaciones de layout para que todas las láminas no repitan la misma estructura.
- Mantener el texto exacto del documento.
- Permitir previsualización rápida y después render final en Cycles.

## Próximo paso concreto

Probar con los tres PNG de portada un archivo Blender de prueba que:

1. cree una escena vertical 1080×1440;
2. configure Cycles;
3. importe un asset como plano con proporción correcta;
4. cree una cámara frontal y una iluminación/material sin alterar los colores;
5. deje el subtítulo como texto editable;
6. guarde el `.blend` y un render de prueba;
7. registre dimensiones, rutas, motor y resultado para poder repetirlo con las siguientes láminas.

No comenzar todavía una nueva investigación general ni volver a decidir la arquitectura: primero validar esta prueba concreta.

## Reglas para futuras sesiones

- Leer este handoff antes de proponer cambios.
- No volver a preguntar si el formato es 1080×1440.
- No volver a preguntar si el PDF tiene imágenes: tiene solo texto.
- No volver a replantear Blender frente a Illustrator: Blender es el núcleo de animación y composición.
- No sustituir los assets actuales ni buscar otros sin autorización.
- No cambiar el texto del PDF.
- No llamar “error” a una espera de Blender sin comprobar primero heartbeat, archivo de respuesta o estado de la instancia.
- Si falta un dato, inspeccionar primero el workspace y este handoff; preguntar solo lo que realmente no pueda determinarse.

## Reconstrucción completa de la sesión

Este documento también conserva el entorno técnico construido durante la
sesión, no solo las decisiones editoriales del carrusel.

### Contexto de trabajo

- El usuario es artista visual, diseñador de Reduciendo Daño y VJ.
- El entorno debe servir para producción propia, herramientas para colegas
  diseñadores/VJ, curaduría personal y materiales de la ONG.
- La base debe separar herramientas comunitarias, evidencia/base de datos y
  curaduría personal.
- La semántica científica puede orientar iconografía, pero no se convierte
  automáticamente en consejo médico ni en una afirmación pública.

## Herramientas instaladas e integradas

### Repositorios locales

| Fuente | Ruta | Función | Estado |
|---|---|---|---|
| thi.ng umbrella | `C:\IA\svg\umbrella` | geometría, SVG, color, interpolación y estructuras | `svg.thi-ng-geom` integrado |
| D3 | `C:\IA\svg\d3` | escalas, layouts, jerarquías y datos a SVG | `data.d3-chart` integrado |
| three.js | `C:\IA\svg\three.js` | preview web, cámara, materiales y prototipos 3D | `scene3d.create` integrado |
| Effect | `C:\IA\svg\effect` | retries, recursos y concurrencia | `workflow.effect-retry` integrado |
| RxJS | `C:\IA\svg\rxjs` | eventos, streams y progreso | `workflow.rxjs-events` integrado |
| stdlib | `C:\IA\svg\stdlib` | estadística, cálculo numérico y señales | integrado con alerta Defender; ver seguridad |
| GDKB 0.6.1 | `C:\IA\svg\agent-toolkit\integrations\gdkb\v0.6.1` | búsqueda semántica, identidad, evidencia y procedencia | bridge Python integrado |

Inventarios persistentes:

- `C:\IA\svg\agent-toolkit\integrations\tool-sources.json`
- `C:\IA\svg\agent-toolkit\integrations\scripting-map.json`
- `C:\IA\svg\agent-toolkit\registry.json`

### Agent Toolkit

Ruta: `C:\IA\svg\agent-toolkit`.

Capacidades principales registradas:

- SVG: crear, incrustar imagen, rasterizar con CairoSVG, vectorizar, animar,
  partículas, validar y previsualizar.
- Geometría thi.ng: `svg.thi-ng-geom`.
- Imágenes: dividir raster/sprite sheet con `image.split`.
- Datos: charts, D3, animación de charts y estadísticas stdlib.
- Preview: escenas HTML con three.js.
- Blender: crear escena, renderizar, importar SVG/raster, generar layout,
  importar/exportar GLB y usar Geometry Nodes.
- Adobe: envelopes de trabajo, consulta de estado y cola para Photoshop,
  Illustrator y After Effects.
- Photoshop: separación por sujeto o regiones, PSD, PNG transparentes y
  manifest. Runtime dependiente de host.
- Búsqueda visual: `asset.search`, `asset.fetch`, `asset.select`.
- Fuentes semánticas: PubChem, ChEBI y OLS para identidad/nomenclatura.
- Iconografía: Iconify y Bioicons como fuentes de SVG editables.
- GDKB: normalización, resolución conservadora, importación, replay,
  snapshots y merges con evidencia.
- Workflows compuestos: documento → storyboard → assets → Photoshop → Blender;
  imagen → SVG → preview → Blender → Illustrator.

Estado global y auditoría: `C:\IA\svg\agent-toolkit\PROJECT-STATUS.md`.

Comandos operativos:

```powershell
cd C:\IA\svg\agent-toolkit
npm run tool -- list
npm run tool -- integration sources
npm run tool -- integration validate
npm run tool -- integration plan --source projects/chemsex/storyboard.json
npm run tool -- workflow document-to-animated-post --document "C:\Users\issvk\claude_sesiones_recuperadas\CARRUSEL CHEMSEX RevCO.pdf"
npm run tool -- photoshop separate-objects --input FILE --mode regions --objects regions.json --output separated/manifest.json --psd-output separated/objects.psd
npm run tool -- blender run --operation layout-scene --spec projects/chemsex/storyboard.json --output jobs/manual/output/chemsex.blend --render-output jobs/manual/output/chemsex.png
```

### Adobe y PDF

- Photoshop 2026: separación por objetos/regiones y exportación PSD/PNG;
  JSX/COM verificado, UXP directo parcial.
- Illustrator 2026: importación/exportación SVG mediante JSX/COM verificada.
- After Effects: adaptador preparado pero runtime pendiente por decisión del
  usuario; no insistir ahora.
- PDF Services API: integrada; el adaptador lee credenciales desde el `.env`
  de `C:\IA\flujo` mediante `PDF_SERVICES_CLIENT_ID`,
  `PDF_SERVICES_CLIENT_SECRET` o una ruta JSON. Nunca guardar valores secretos
  aquí.
- Firefly: el usuario tiene créditos de la aplicación, pero Firefly Services
  API no quedó confirmada. La generación visual usada fue manual.
- Panel Adobe existente: `C:\IA\flujo\tools\adobe_panel`.

## Artefactos ya creados

Contratos de Chemsex:

- `C:\IA\svg\agent-toolkit\projects\chemsex\PROJECT.json`
- `C:\IA\svg\agent-toolkit\projects\chemsex\storyboard.json`
- `C:\IA\svg\agent-toolkit\projects\chemsex\concept-map.json`
- `C:\IA\svg\agent-toolkit\projects\chemsex\research-interactions.json`
- `C:\IA\svg\agent-toolkit\INTEGRATION-GUIDE.md`
- `C:\IA\svg\agent-toolkit\adapters\blender\GEOMETRY-NODES.md`

El proyecto declara canvas `1080×1440`, texto en orden literal, raíces para
assets/PSD/Blender/manifests/renders, separación Photoshop opcional, layout de
Geometry Nodes y Cycles obligatorio.

Variantes visuales generadas durante la sesión:

- `projects\chemsex\generated\slide-06-care-flat-v1.png`
- `projects\chemsex\generated\slide-06-care-flat-v2.png`
- `projects\chemsex\generated\slide-06-care-open-palette-v3.png`
- `projects\chemsex\generated\slide-06-care-open-palette-v4.png`
- `projects\chemsex\generated\slide-07-interactions-flat-v1.png`
- `projects\chemsex\generated\slide-07-interactions-flat-v2.png`
- `projects\chemsex\generated\slide-07-interactions-open-palette-v3.png`
- `projects\chemsex\generated\slide-08-close-flat-v1.png` a `v6.png`

Son exploraciones del asistente y no sustituyen los assets seleccionados por
el usuario desde Firefly.

## Prompts y dirección visual recuperada

Los prompts de Firefly se definieron en inglés y desde cero. Firefly no debe
generar tipografía final: el texto exacto se incorpora como texto editable en
Blender o Adobe.

### Prompt base

```text
Flat editorial illustration for a harm-reduction Instagram carousel, vertical
1080x1440 composition, contemporary queer community and nightlife context,
clear symbolic visual language, layered shapes, subtle paper grain, controlled
texture, strong silhouette design, expressive but accessible, informative
without looking like a medical brochure, warm human presence, flexible open
color palette, balanced negative space for editable text, no generated words,
no logos, no watermark, no photorealism, no explicit sexual imagery, no drug
glamour, no generic nightclub stock image.
```

### Lámina 2 — definición

```text
Flat editorial illustration about chemsex as psychoactive substances used in
sexual contexts, represented through two connected visual fields: altered
perception and collective care. Use an abstract network, a soft waveform and a
protective membrane, with one calm text-safe area and one stronger illustration
area. Contemporary community feeling, nuanced and non-moralizing, controlled
texture, open color palette. No literal pill lineup, no explicit bodies, no
medical infographic, no generated text.
```

### Lámina 3 — reducción de daños / contexto

```text
Flat editorial illustration showing harm reduction as a connected system of
care. Use linked nodes, a conversation gesture, a protective network and an
abstract map of different social contexts: private rooms, public-space
thresholds and mobile-app connections. Keep the visual relational rather than
literal. Contemporary techno-nightlife audience, diverse urban clothing,
subtle movement, warm community energy. No plants, no stereotypes, no anonymous
crowd, no substance glamour, no generated text.
```

### Lámina 4 — sustancias

```text
Flat editorial visual system for common substances in a local chemsex context.
Represent the substances as distinct abstract nodes in a constellation with
different shapes, textures and color signals, not as a product lineup. Make the
relationships and context more important than the objects themselves. Dynamic
asymmetrical composition, clear space for exact text, editorial texture,
contemporary queer nightlife atmosphere. No dosage information, no brand-like
packaging, no photorealistic pills, no drug glamour, no generated text.
```

### Lámina 5 — riesgos generales

```text
Flat editorial illustration of a fragile interconnected system under several
pressures: heart rhythm, warning signal, infection risk, altered mental state
and post-session vulnerability. Use broken or overloaded network lines and
contrasting rhythm fields, but keep the tone educational and humane. Strong
visual hierarchy, dynamic composition, open palette, room for exact text. No
gore, no fear-porn, no death imagery, no sensational medical symbols, no
generated text.
```

### Lámina 6 — cómo cuidarnos

```text
Flat editorial illustration about community care in a techno-nightlife harm-
reduction context. Show a connected network of diverse young adults with subtle
urban clothing, a shared water droplet, a testing symbol, protective links and
a calm consent conversation. The people should feel contemporary and natural,
not stereotyped, not elderly, not posed like stock characters. Use a richer
open palette with teal, coral, orange, lilac, green and warm neutrals; keep
the image friendly and informative, not excessively minimal or clinical. No
plants, no drug glamour, no medical uniforms, no generated text.
```

### Lámina 7 — interacciones

```text
Flat editorial diagrammatic illustration about risky drug interactions. Use
separate streams that collide or overload a shared heart-and-pressure network:
descending waves, competing pulse lines, a pressure imbalance and a clear
critical threshold. Make each interaction visually distinct and avoid one
repeated centered icon. Use asymmetry, layered depth and an open color palette
while keeping the message legible and non-sensational. No dosage guidance, no
product advertising, no graphic injury, no generated text.
```

### Lámina 8 — cierre / comunidad

```text
Warm flat editorial illustration for a community harm-reduction closing slide.
Show a connected network of diverse contemporary people, hands or gestures of
mutual support, soft links and a shared protective field. The composition should
feel open, alive and communal rather than cold or sterile. Use the established
editorial texture and an expanded palette beyond repeated navy blue. Keep the
visual dynamic, leave a clear area for exact closing text, and avoid plants,
generic wellness imagery, clichéd hairstyles, stereotyped bodies, generated
words and medical-poster aesthetics.
```

Aprendizaje visual de las iteraciones:

- La primera dirección quedó demasiado cargada; la siguiente demasiado
  minimalista. El punto correcto es plano/editorial con textura, ritmo, capas y
  gestos humanos.
- Se repitió demasiado “texto arriba / ilustración abajo”. El sistema debe
  alternar lateralidad, diagonal, banda inferior, texto integrado y campo
  completo.
- La paleta no debe quedar atrapada en azul navy: puede abrirse a teal, coral,
  naranja, lilac, verde y neutros cálidos.
- Las redes, conexiones y contención funcionan mejor que plantas decorativas
  para el concepto de cuidado.
- Evitar clichés de asistentes techno: peinados reconocibles como “señora”,
  cuerpos genéricos, ropa estereotipada o fiesta literal.
- El texto final debe quedar fuera del generador de imagen.

## Aprendizaje técnico consolidado

1. El PDF es fuente editorial de texto, no fuente visual.
2. Los recuadros del storyboard son guías matemáticas de espacio, no objetos
   finales.
3. Texto, assets, zonas y transformaciones viajan como JSON/manifests, no como
   una escena opaca.
4. Photoshop es la etapa correcta cuando un raster debe separarse por objetos
   y conservar PSD editable.
5. Illustrator sirve para ilustración vectorial estática, limpieza y export;
   Blender es el compositor y animador final.
6. SVG se importa como curvas cuando es posible; mesh solo cuando Geometry
   Nodes lo necesita.
7. CairoSVG es fallback visual para filtros, texto o gradientes que no puedan
   representarse como curvas; el SVG fuente se conserva.
8. SVG y PNG usan materiales emisión/sRGB para que Cycles no oscurezca colores
   planos ni agrave solapamientos de capas.
9. Cada asset debe recibir controles de escala, offset, rotación, profundidad y
   pulso; Geometry Nodes debe ser el lugar de animación.
10. La composición automática debe medir carga de texto, márgenes, área de
    ilustración, relación entre ambos y una variante de layout.
11. El addon grande es la dirección correcta, pero primero se validan contratos
    y una prueba vertical reproducible antes de convertir todo en UI.

## Auditoría SSH / MAK

El usuario proporcionó el contexto de conexión a MAK y sus límites operativos.
Debe conservarse para futuras sesiones:

- Equipo: `dell-11m`, Debian 12.
- Usuario: `mak`.
- Puerto: `22`.
- IP primaria: `10.242.182.85`.
- Fallback Ethernet: `192.168.50.2`.
- Runtime activo: `/home/mak/*`.
- `/home/mak/WIN` es archivo histórico/evidencia, no runtime.

Contexto mínimo solicitado al conectar:

```bash
sed -n '1,240p' /home/mak/flujo/agents.md
sed -n '1,260p' /home/mak/flujo/context/LAST_HANDOFF.md
sed -n '1,220p' /home/mak/flujo/CAPACIDADES.md
sed -n '1,180p' /home/mak/flujo/README.md
```

Para la investigación de plantas se solicitó además leer únicamente los
archivos indicados por el usuario en `curatoria_inbox`, `research/jobs/3` y
`flujo/tools`.

Reglas MAK:

- No clonar ni copiar árboles completos.
- No usar Git como inventario.
- No leer todos los Markdown/Python.
- No mostrar, copiar ni modificar secretos, `.env`, claves API o credenciales.
- No instalar paquetes ni iniciar servicios permanentes.
- No borrar evidencia ni bases de datos.
- Toda búsqueda debe contemplar español e inglés ASCII.
- Antes de editar, informar archivo exacto y motivo.
- Toda conclusión debe registrar ruta, evidencia, comando y resultado.

**Estado de evidencia:** este workspace no contiene una transcripción
persistente de los comandos ni de los resultados de una sesión SSH a MAK. Por
tanto, el protocolo y las rutas quedan registrados, pero no se deben inventar
conclusiones detalladas sobre el estado remoto. Antes de afirmar un dato de MAK
hay que reconectar y verificarlo con los comandos mínimos anteriores.

## Incidente de seguridad: Stdlib

Archivo detectado:

`C:\IA\svg\stdlib\lib\node_modules\@stdlib\ndarray\base\diagonal\docs\types\test.ts`

Defender registró:

- amenaza: `Trojan:JS/StrelaStealer.GXU!MTB`;
- `DidThreatExecute: False`;
- `IsActive: False`;
- acción de cuarentena exitosa;
- el archivo ya no está presente.

Procedencia comprobada:

- ZIP: `C:\Users\issvk\Downloads\stdlib-develop.zip`;
- SHA-256 del ZIP: `0471A6E0E73AAEC7C041412DF28942E2D3550C51E3F348ABB55E2193936155EF`;
- `Zone.Identifier`: `https://codeload.github.com/stdlib-js/stdlib/zip/refs/heads/develop`;
- el ZIP contiene la ruta exacta del archivo detectado;
- `package.json` identifica `@stdlib/ndarray`, licencia Apache-2.0 y el
  repositorio oficial de Stdlib;
- la fuente pública del archivo contiene pruebas TypeScript de tipos y
  anotaciones `$ExpectError`, no un ejecutable.

Conclusión operativa: la evidencia favorece un falso positivo o detección
heurística sobre un fixture legítimo, pero no permite certificar el archivo
local porque fue puesto en cuarentena antes de obtener su hash. No restaurar ni
ejecutar el archivo. No ejecutar `npm install`, `npm test` ni scripts de Stdlib
hasta decidir si se reemplaza el snapshot por una fuente/version verificada.
Stdlib no es necesaria para la prueba inmediata de Blender/Cycles.

## Errores y correcciones que deben conservarse

- Tratar el PDF como si tuviera portada o imágenes → el PDF solo aporta texto.
- Confundir el canvas con otras medidas → el formato cerrado es 1080×1440.
- Proponer demasiadas láminas o diez láminas → mantener ocho y continuidad.
- Mostrar assets del usuario o seguir buscando imágenes sin autorización → usar
  los tres PNG de Firefly ya identificados.
- Repetir texto en la misma zona → layout dinámico parametrizado.
- Pasar de una imagen cargada a una demasiado fría → plano/editorial con
  textura, red, capas, color y comunidad.
- Volver a discutir Blender → Blender es núcleo, Geometry Nodes controla y
  Cycles es obligatorio.
- Buscar handoffs fuera de este workspace para reconstruir una conversación →
  este archivo es la memoria del proyecto; no abrir otras carpetas como
  sustituto del chat sin autorización.
- `OS error 10053` → conexión abortada por Windows; no implica por sí mismo
  corrupción local ni autoriza a disfrazar tráfico.

## Estado final de la sesión

### Confirmado

- Proyecto Chemsex con ocho láminas, 1080×1440 y texto exacto.
- Storyboard, mapa conceptual, investigación de interacciones y proyecto JSON.
- Variantes visuales para láminas 6, 7 y 8.
- Adapters declarativos para SVG, imagen, Blender, Adobe, GDKB, D3, three.js,
  Effect, RxJS y stdlib.
- Blender/Cycles/Geometry Nodes como arquitectura elegida.
- Tres assets de portada entregados por el usuario.
- Origen del snapshot Stdlib y estado de cuarentena documentados.

### Parcial / host-dependiente

- Photoshop requiere la aplicación abierta para producir PSD y manifest real.
- Firefly Services API no está confirmada.
- After Effects queda pendiente.
- Illustrator y Photoshop tienen rutas JSX/COM comprobadas; UXP directo no está
  completamente validado.

### No confirmado

- No está documentado en este workspace el resultado reproducible de la sesión
  SSH a MAK; verificar remotamente antes de afirmar estado actual.
- No está validado todavía el render final de portada con los PNG reales del
  usuario dentro de una escena Blender editable.
- No debe afirmarse que Stdlib está limpia hasta reemplazar/verificar el
  archivo puesto en cuarentena.

## Próxima acción única

Construir una prueba aislada de portada en Blender 4.5.4 LTS si esa instalación
está disponible:

1. usar uno de los PNG del usuario;
2. crear canvas 1080×1440;
3. configurar Cycles;
4. importar el PNG como textura sRGB/emisión;
5. añadir `Orgullo es cuidarnos en comunidad` como texto editable;
6. conservar el PNG original y la composición separada;
7. producir un `.blend` y un render de prueba;
8. registrar resultado y rutas en el manifest.

No hacer otra investigación general, no volver a decidir el motor y no
reconstruir el storyboard desde el PDF.
