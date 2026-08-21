import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

const here = path.dirname(fileURLToPath(import.meta.url))
const iconDir = path.resolve(here, "../../../rd_database_complete/assets/generated_icons")
const backgroundPath = "C:\\Users\\issvk\\.codex\\generated_images\\01a01361-7f6d-76b0-b1b1-f4c1c81197fe\\exec-65166eda-9c66-4490-983d-b8130f346265.png"
const outputDir = path.join(here, "generated", "slide-04-substances")
const svgPath = path.join(outputDir, "slide-04-diorama-local.svg")
fs.mkdirSync(outputDir, { recursive: true })

const pngUri = (filename) => `data:image/png;base64,${fs.readFileSync(filename).toString("base64")}`
const iconUri = (filename) => pngUri(path.join(iconDir, filename))
const bgUri = pngUri(backgroundPath)

const icon = ({ file, x, y, size, rotation, accent, opacity = 1 }) => {
  const cx = x + size / 2
  const cy = y + size / 2
  return `
    <g transform="rotate(${rotation} ${cx} ${cy})" opacity="${opacity}">
      <circle cx="${cx}" cy="${cy}" r="${size * .42}" fill="${accent}" opacity=".2" filter="url(#softGlow)"/>
      <image href="${iconUri(file)}" x="${x}" y="${y}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet" filter="url(#iconShadow)"/>
    </g>`
}

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440" role="img" aria-labelledby="title desc">
  <title id="title">Composición de diorama sin texto para la lámina 4 de Chemsex</title>
  <desc id="desc">Placa arquitectónica 3D con ocho iconos editoriales integrados en diferentes espacios y un muro vacío para texto.</desc>
  <defs>
    <filter id="softGlow"><feGaussianBlur stdDeviation="20"/></filter>
    <filter id="iconShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#03040c" flood-opacity=".75"/>
    </filter>
    <linearGradient id="glassA" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#8c76ff" stop-opacity=".22"/>
      <stop offset=".5" stop-color="#58e8f2" stop-opacity=".08"/>
      <stop offset="1" stop-color="#ff6b8c" stop-opacity=".18"/>
    </linearGradient>
    <linearGradient id="glassB" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="#ff9c55" stop-opacity=".15"/>
      <stop offset="1" stop-color="#7b5aff" stop-opacity=".12"/>
    </linearGradient>
  </defs>

  <image href="${bgUri}" x="0" y="0" width="1080" height="1440" preserveAspectRatio="none"/>

  <!-- Local SVG glass planes make the icon placements feel spatial rather than catalogued. -->
  <path d="M20 74 L300 42 L314 300 L18 336 Z" fill="url(#glassA)" stroke="#8f78ff" stroke-opacity=".38" stroke-width="3"/>
  <path d="M172 292 L480 276 L492 548 L154 566 Z" fill="url(#glassB)" stroke="#58e8f2" stroke-opacity=".32" stroke-width="3"/>
  <path d="M10 650 L300 642 L314 892 L8 914 Z" fill="#ff745f" fill-opacity=".07" stroke="#ff9b71" stroke-opacity=".28" stroke-width="3"/>
  <path d="M178 936 L486 914 L500 1202 L162 1230 Z" fill="url(#glassA)" stroke="#58e8f2" stroke-opacity=".24" stroke-width="3"/>

  <!-- Eight exact library icons, placed as objects in separate architectural depths. -->
  ${icon({ file: "amphetamine.png", x: 32, y: 100, size: 176, rotation: -13, accent: "#ffb735" })}
  ${icon({ file: "mdma.png", x: 248, y: 118, size: 148, rotation: 12, accent: "#ff638f" })}
  ${icon({ file: "cannabis.png", x: 22, y: 365, size: 172, rotation: -18, accent: "#9bd94d" })}
  ${icon({ file: "alkyl_nitrites.png", x: 298, y: 392, size: 138, rotation: 15, accent: "#54dce9" })}
  ${icon({ file: "cocaine.png", x: 32, y: 700, size: 174, rotation: -6, accent: "#f1e2c2" })}
  ${icon({ file: "ketamine.png", x: 300, y: 670, size: 136, rotation: 10, accent: "#7eaaff" })}
  ${icon({ file: "methamphetamine.png", x: 58, y: 1004, size: 178, rotation: -12, accent: "#2bc9ef" })}
  ${icon({ file: "ghb_gbl.png", x: 310, y: 1018, size: 144, rotation: 8, accent: "#8bbcff" })}

  <!-- Keep the generated architectural wall on the right quiet for editable copy. -->
  <path d="M612 60 C760 34 924 60 1046 120" fill="none" stroke="#b98cff" stroke-opacity=".12" stroke-width="2" stroke-dasharray="2 20"/>
  <path d="M646 1130 C780 1090 916 1150 1048 1088" fill="none" stroke="#54dce9" stroke-opacity=".1" stroke-width="2" stroke-dasharray="2 20"/>
</svg>
`

fs.writeFileSync(svgPath, svg, "utf8")
console.log(JSON.stringify({ svg: svgPath, iconCount: 8, textElements: 0, background: backgroundPath }, null, 2))
