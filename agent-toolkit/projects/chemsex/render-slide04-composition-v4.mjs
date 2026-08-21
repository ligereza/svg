import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

const here = path.dirname(fileURLToPath(import.meta.url))
const iconDir = path.resolve(here, "../../../rd_database_complete/assets/generated_icons")
const outputDir = path.join(here, "generated", "slide-04-substances")
const svgPath = path.join(outputDir, "slide-04-composition-v4.svg")
fs.mkdirSync(outputDir, { recursive: true })

const dataUri = (filename) => `data:image/png;base64,${fs.readFileSync(path.join(iconDir, filename)).toString("base64")}`

const icon = ({ file, x, y, size, rotation, accent, opacity = 1 }) => {
  const image = dataUri(file)
  const cx = x + size / 2
  const cy = y + size / 2
  return `
    <g transform="rotate(${rotation} ${cx} ${cy})" opacity="${opacity}">
      <circle cx="${cx}" cy="${cy}" r="${size * .43}" fill="${accent}" opacity=".1" filter="url(#blur24)"/>
      <image href="${image}" x="${x}" y="${y}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet"/>
    </g>`
}

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440" role="img" aria-labelledby="title desc">
  <title id="title">Composición visual sin texto para la lámina 4 de Chemsex</title>
  <desc id="desc">Collage prismático de ocho iconos editoriales y un espacio limpio reservado para texto.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#070913"/>
      <stop offset=".42" stop-color="#17183b"/>
      <stop offset="1" stop-color="#080a14"/>
    </linearGradient>
    <radialGradient id="violetGlow" cx="22%" cy="45%" r="62%">
      <stop offset="0" stop-color="#995fff" stop-opacity=".42"/>
      <stop offset=".5" stop-color="#28388b" stop-opacity=".17"/>
      <stop offset="1" stop-color="#080a14" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="textField" cx="35%" cy="45%" r="74%">
      <stop offset="0" stop-color="#fa8d76" stop-opacity=".16"/>
      <stop offset=".55" stop-color="#a85582" stop-opacity=".05"/>
      <stop offset="1" stop-color="#080a14" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="planeA" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#7b4fff" stop-opacity=".48"/>
      <stop offset="1" stop-color="#27dbe7" stop-opacity=".13"/>
    </linearGradient>
    <linearGradient id="planeB" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ff527f" stop-opacity=".38"/>
      <stop offset="1" stop-color="#ffb23e" stop-opacity=".15"/>
    </linearGradient>
    <linearGradient id="planeC" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="#38dce6" stop-opacity=".28"/>
      <stop offset="1" stop-color="#a57eff" stop-opacity=".12"/>
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
  <rect x="16" y="16" width="1048" height="1408" fill="url(#bg)"/>
  <rect x="16" y="16" width="1048" height="1408" fill="url(#violetGlow)"/>
  <rect x="520" y="16" width="544" height="1408" fill="url(#textField)"/>
  <ellipse cx="322" cy="740" rx="280" ry="600" fill="#8a5cff" opacity=".12" filter="url(#blur80)"/>

  <!-- One large irregular prism: the icons belong to this single form. -->
  <path d="M126 88 L518 42 L628 270 L530 520 L628 758 L532 1118 L392 1354 L88 1286 L146 1000 L76 748 L152 514 L94 284 Z" fill="#111630" fill-opacity=".62" stroke="#b98cff" stroke-opacity=".3" stroke-width="3"/>
  <path d="M126 88 L360 66 L430 310 L152 514 L94 284 Z" fill="url(#planeA)" fill-opacity=".75"/>
  <path d="M360 66 L518 42 L628 270 L430 310 Z" fill="url(#planeB)" fill-opacity=".78"/>
  <path d="M430 310 L628 270 L530 520 L152 514 Z" fill="#ff668c" fill-opacity=".18"/>
  <path d="M152 514 L530 520 L628 758 L76 748 Z" fill="url(#planeC)" fill-opacity=".66"/>
  <path d="M76 748 L628 758 L532 1118 L132 1000 Z" fill="url(#planeA)" fill-opacity=".42"/>
  <path d="M132 1000 L532 1118 L392 1354 L88 1286 Z" fill="url(#planeB)" fill-opacity=".34"/>

  <!-- Layered cut-paper edges, deliberately not a grid or a route. -->
  <path d="M146 514 L430 310 L530 520 L256 698 Z" fill="none" stroke="#fff" stroke-opacity=".16" stroke-width="5"/>
  <path d="M76 748 L530 520 L628 758 L132 1000 Z" fill="none" stroke="#59e5ed" stroke-opacity=".22" stroke-width="5"/>
  <path d="M132 1000 L628 758" fill="none" stroke="#ffb33f" stroke-opacity=".18" stroke-width="3" stroke-dasharray="2 16"/>

  <!-- Full icons integrated into different planes, with varied scale and depth. -->
  ${icon({ file: "amphetamine.png", x: 48, y: 102, size: 236, rotation: -18, accent: "#ffb735" })}
  ${icon({ file: "mdma.png", x: 292, y: 72, size: 210, rotation: 13, accent: "#ff638f" })}
  ${icon({ file: "cannabis.png", x: 64, y: 346, size: 222, rotation: -24, accent: "#9bd94d" })}
  ${icon({ file: "alkyl_nitrites.png", x: 372, y: 316, size: 178, rotation: 20, accent: "#54dce9" })}
  ${icon({ file: "cocaine.png", x: 174, y: 540, size: 256, rotation: -8, accent: "#f1e2c2" })}
  ${icon({ file: "ketamine.png", x: 24, y: 724, size: 172, rotation: 15, accent: "#7eaaff" })}
  ${icon({ file: "methamphetamine.png", x: 352, y: 732, size: 228, rotation: -12, accent: "#2bc9ef" })}
  ${icon({ file: "ghb_gbl.png", x: 228, y: 1012, size: 190, rotation: 12, accent: "#8bbcff" })}

  <!-- Right side stays open for the later editable copy. -->
  <path d="M680 230 C802 168 946 226 1005 344" fill="none" stroke="#ff9b80" stroke-opacity=".2" stroke-width="3" stroke-dasharray="2 20"/>
  <path d="M664 1118 C786 1052 920 1120 1018 1034" fill="none" stroke="#54dce9" stroke-opacity=".18" stroke-width="3" stroke-dasharray="2 20"/>
  <circle cx="730" cy="256" r="6" fill="#ffb735" opacity=".75"/>
  <circle cx="952" cy="346" r="7" fill="#ff638f" opacity=".75"/>
  <circle cx="748" cy="1112" r="5" fill="#a980ff" opacity=".75"/>
  <circle cx="982" cy="1034" r="6" fill="#54dce9" opacity=".75"/>

  <rect x="16" y="16" width="1048" height="1408" fill="url(#grain)"/>
  <g opacity=".8">
    <circle cx="1008" cy="1312" r="8" fill="#ff638f"/>
    <circle cx="1034" cy="1312" r="8" fill="#54dce9"/>
    <circle cx="1060" cy="1312" r="8" fill="#ffb735"/>
  </g>
</svg>
`

fs.writeFileSync(svgPath, svg, "utf8")
console.log(JSON.stringify({ svg: svgPath, iconCount: 8, textElements: 0 }, null, 2))
