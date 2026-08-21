import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

const here = path.dirname(fileURLToPath(import.meta.url))
const iconDir = path.resolve(here, "../../../rd_database_complete/assets/generated_icons")
const outputDir = path.join(here, "generated", "slide-04-substances")
const svgPath = path.join(outputDir, "slide-04-composition-v3.svg")

fs.mkdirSync(outputDir, { recursive: true })

const dataUri = (filename) => `data:image/png;base64,${fs.readFileSync(path.join(iconDir, filename)).toString("base64")}`

const icon = ({ file, x, y, size, rotation, accent, opacity = 1 }) => {
  const image = dataUri(file)
  const cx = x + size / 2
  const cy = y + size / 2
  return `
    <g transform="rotate(${rotation} ${cx} ${cy})" opacity="${opacity}">
      <circle cx="${cx}" cy="${cy}" r="${size * .42}" fill="${accent}" opacity=".09" filter="url(#blur24)"/>
      <circle cx="${cx}" cy="${cy}" r="${size * .43}" fill="none" stroke="${accent}" stroke-opacity=".28" stroke-width="2" stroke-dasharray="2 18"/>
      <image href="${image}" x="${x}" y="${y}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet"/>
    </g>`
}

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440" role="img" aria-labelledby="title desc">
  <title id="title">Composición visual sin texto para la lámina 4 de Chemsex</title>
  <desc id="desc">Ocho iconos editoriales dispuestos como una trayectoria orgánica y un campo libre para texto editable.</desc>
  <defs>
    <linearGradient id="base" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#090b18"/>
      <stop offset=".42" stop-color="#241849"/>
      <stop offset="1" stop-color="#080a14"/>
    </linearGradient>
    <radialGradient id="violet" cx="25%" cy="38%" r="60%">
      <stop offset="0" stop-color="#7f52ff" stop-opacity=".48"/>
      <stop offset=".48" stop-color="#263a89" stop-opacity=".2"/>
      <stop offset="1" stop-color="#080a14" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="emptyField" cx="30%" cy="45%" r="75%">
      <stop offset="0" stop-color="#f07c84" stop-opacity=".19"/>
      <stop offset=".45" stop-color="#d26b82" stop-opacity=".07"/>
      <stop offset="1" stop-color="#080a14" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="trail" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffb735"/>
      <stop offset=".33" stop-color="#ff638f"/>
      <stop offset=".66" stop-color="#59e4ed"/>
      <stop offset="1" stop-color="#a980ff"/>
    </linearGradient>
    <filter id="blur24"><feGaussianBlur stdDeviation="24"/></filter>
    <filter id="blur80"><feGaussianBlur stdDeviation="80"/></filter>
    <pattern id="grain" width="52" height="52" patternUnits="userSpaceOnUse">
      <circle cx="5" cy="8" r="1" fill="#fff" opacity=".05"/>
      <circle cx="30" cy="23" r="1" fill="#fff" opacity=".035"/>
      <circle cx="42" cy="43" r="1" fill="#fff" opacity=".04"/>
      <path d="M12 35l5-2M34 7l5 2" stroke="#fff" stroke-opacity=".025"/>
    </pattern>
  </defs>

  <rect width="1080" height="1440" fill="#080a14"/>
  <rect x="16" y="16" width="1048" height="1408" fill="url(#base)"/>
  <rect x="16" y="16" width="1048" height="1408" fill="url(#violet)"/>

  <!-- Clear, irregular text field: intentionally quiet but not a blank rectangle. -->
  <path d="M604 74 C788 10 1016 100 1036 294 C1055 482 945 550 1002 742 C1065 952 1004 1198 820 1368 L1064 1424 L1064 16 L654 16 Z" fill="url(#emptyField)"/>
  <path d="M646 148 C790 84 942 142 976 258 C1006 365 924 448 962 562" fill="none" stroke="#ff9d88" stroke-opacity=".18" stroke-width="3" stroke-dasharray="2 20"/>

  <rect x="16" y="16" width="1048" height="1408" fill="url(#grain)"/>

  <!-- One continuous S-shaped visual current; it replaces the list/grid logic. -->
  <path d="M104 238 C260 74 488 122 458 300 C430 470 106 415 96 600 C84 788 487 644 520 830 C552 1016 186 972 130 1182 C100 1290 250 1352 426 1260" fill="none" stroke="url(#trail)" stroke-opacity=".65" stroke-width="7" stroke-linecap="round"/>
  <path d="M104 238 C260 74 488 122 458 300 C430 470 106 415 96 600 C84 788 487 644 520 830 C552 1016 186 972 130 1182 C100 1290 250 1352 426 1260" fill="none" stroke="#fff" stroke-opacity=".11" stroke-width="22" stroke-linecap="round" filter="url(#blur24)"/>

  <!-- Deliberately irregular placement: no rows, no columns, no repeated card treatment. -->
  ${icon({ file: "amphetamine.png", x: 52, y: 92, size: 244, rotation: -21, accent: "#ffb735" })}
  ${icon({ file: "mdma.png", x: 316, y: 64, size: 202, rotation: 17, accent: "#ff638f" })}
  ${icon({ file: "cannabis.png", x: 88, y: 330, size: 222, rotation: -29, accent: "#9bd94d" })}
  ${icon({ file: "alkyl_nitrites.png", x: 356, y: 322, size: 174, rotation: 23, accent: "#54dce9" })}
  ${icon({ file: "cocaine.png", x: 190, y: 540, size: 258, rotation: -9, accent: "#f1e2c2" })}
  ${icon({ file: "ketamine.png", x: 40, y: 704, size: 166, rotation: 18, accent: "#7eaaff" })}
  ${icon({ file: "methamphetamine.png", x: 364, y: 730, size: 224, rotation: -16, accent: "#2bc9ef" })}
  ${icon({ file: "ghb_gbl.png", x: 238, y: 1018, size: 192, rotation: 13, accent: "#8bbcff" })}

  <!-- Small visual anchors keep the open field intentional, without becoming text or a list. -->
  <g fill="none" stroke-linecap="round" opacity=".38">
    <path d="M622 820 C706 748 832 802 1005 728" stroke="#54dce9" stroke-width="2" stroke-dasharray="2 18"/>
    <path d="M654 1192 C764 1126 864 1212 1016 1144" stroke="#ff9c74" stroke-width="2" stroke-dasharray="2 18"/>
    <circle cx="720" cy="812" r="6" fill="#54dce9" stroke="none"/>
    <circle cx="926" cy="762" r="5" fill="#ffb735" stroke="none"/>
    <circle cx="772" cy="1188" r="5" fill="#a980ff" stroke="none"/>
    <circle cx="978" cy="1158" r="7" fill="#ff638f" stroke="none"/>
  </g>

  <g opacity=".8">
    <circle cx="1008" cy="1312" r="8" fill="#ff638f"/>
    <circle cx="1034" cy="1312" r="8" fill="#54dce9"/>
    <circle cx="1060" cy="1312" r="8" fill="#ffb735"/>
  </g>
</svg>
`

fs.writeFileSync(svgPath, svg, "utf8")
console.log(JSON.stringify({ svg: svgPath, iconCount: 8, textElements: 0 }, null, 2))
