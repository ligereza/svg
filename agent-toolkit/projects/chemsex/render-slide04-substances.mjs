import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

const here = path.dirname(fileURLToPath(import.meta.url))
const iconDir = path.resolve(here, "../../../rd_database_complete/assets/generated_icons")
const outputDir = path.join(here, "generated", "slide-04-substances")
const svgPath = path.join(outputDir, "slide-04-substances-v1.svg")

fs.mkdirSync(outputDir, { recursive: true })

const esc = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")

const dataUri = (filename) => `data:image/png;base64,${fs.readFileSync(path.join(iconDir, filename)).toString("base64")}`

const icons = [
  ["amphetamine.png", "#ffae32"],
  ["mdma.png", "#ff668c"],
  ["cannabis.png", "#9ad94e"],
  ["alkyl_nitrites.png", "#51d9ee"],
  ["cocaine.png", "#e9e1cb"],
  ["ketamine.png", "#7eaaff"],
  ["methamphetamine.png", "#2ac9ef"],
  ["ghb_gbl.png", "#8bbcff"],
]

const positions = [
  [82, 270], [285, 270],
  [82, 500], [285, 500],
  [82, 730], [285, 730],
  [82, 960], [285, 960],
]

const card = (filename, accent, x, y, index) => {
  const image = dataUri(filename)
  return `
    <g>
      <rect x="${x}" y="${y}" width="170" height="170" rx="28" fill="#11152d" fill-opacity=".88" stroke="${accent}" stroke-opacity=".72" stroke-width="3"/>
      <circle cx="${x + 28}" cy="${y + 28}" r="15" fill="${accent}" fill-opacity=".95"/>
      <text x="${x + 28}" y="${y + 34}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="14" font-weight="800" fill="#07101b">${String(index).padStart(2, "0")}</text>
      <image href="${image}" x="${x + 16}" y="${y + 16}" width="138" height="138" preserveAspectRatio="xMidYMid meet"/>
    </g>`
}

const listItems = [
  "Éxtasis (pasti o pilas)",
  "MDMA",
  "Marihuana",
  "Popper",
  "Cocaína",
  "Ketamina",
  "Metanfetamina (cristal)",
  "GHB",
]

const list = listItems.map((item, index) => {
  const y = 444 + index * 76
  const accent = icons[index][1]
  return `
    <g>
      <circle cx="574" cy="${y - 8}" r="7" fill="${accent}"/>
      <text x="598" y="${y}" font-family="Inter,Arial,sans-serif" font-size="27" font-weight="600" fill="#f5f3f4">${esc(item)}</text>
    </g>`
}).join("\n")

const iconCards = icons.map(([filename, accent], index) => card(filename, accent, positions[index][0], positions[index][1], index + 1)).join("\n")

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1080" height="1440" viewBox="0 0 1080 1440" role="img" aria-labelledby="title desc">
  <title id="title">El contexto en Chile</title>
  <desc id="desc">Ocho iconos editoriales de sustancias y su listado literal para la lámina 4 del carrusel Chemsex.</desc>
  <defs>
    <radialGradient id="bgGlow" cx="19%" cy="46%" r="65%">
      <stop offset="0" stop-color="#31205e" stop-opacity=".85"/>
      <stop offset=".48" stop-color="#101938" stop-opacity=".75"/>
      <stop offset="1" stop-color="#070913" stop-opacity="1"/>
    </radialGradient>
    <linearGradient id="warmGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ff4e9b" stop-opacity=".46"/>
      <stop offset=".5" stop-color="#ff8b36" stop-opacity=".28"/>
      <stop offset="1" stop-color="#ffcc4a" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#b98cff"/>
      <stop offset=".5" stop-color="#50e6f0"/>
      <stop offset="1" stop-color="#ff8b50" stop-opacity="0"/>
    </linearGradient>
    <filter id="blur40"><feGaussianBlur stdDeviation="40"/></filter>
    <filter id="blur12"><feGaussianBlur stdDeviation="12"/></filter>
    <pattern id="grain" width="52" height="52" patternUnits="userSpaceOnUse">
      <circle cx="4" cy="9" r="1" fill="#fff" opacity=".05"/>
      <circle cx="29" cy="20" r="1" fill="#fff" opacity=".035"/>
      <circle cx="41" cy="46" r="1" fill="#fff" opacity=".04"/>
      <path d="M10 34l6-2M35 7l4 2" stroke="#fff" stroke-opacity=".025"/>
    </pattern>
  </defs>

  <rect width="1080" height="1440" fill="#070913"/>
  <rect x="16" y="16" width="1048" height="1408" rx="3" fill="url(#bgGlow)"/>
  <ellipse cx="865" cy="820" rx="350" ry="570" fill="url(#warmGlow)" filter="url(#blur40)"/>
  <ellipse cx="210" cy="570" rx="270" ry="430" fill="#8e55ff" opacity=".13" filter="url(#blur40)"/>
  <rect x="16" y="16" width="1048" height="1408" fill="url(#grain)"/>

  <g opacity=".45" fill="none" stroke-linecap="round">
    <path d="M52 222 C150 160 202 236 258 194 S350 168 458 248" stroke="#6e58d9" stroke-width="2"/>
    <path d="M68 1200 C184 1136 252 1238 328 1162 S422 1118 496 1180" stroke="#43dbe7" stroke-width="2"/>
    <path d="M486 180 C536 208 538 250 494 286" stroke="#ff7e8e" stroke-width="2"/>
  </g>

  <path d="M82 118 H286" stroke="url(#rule)" stroke-width="5" stroke-linecap="round"/>

  ${iconCards}

  <g>
    <text x="540" y="150" font-family="Inter,Arial,sans-serif" font-size="58" font-weight="800" letter-spacing="-2" fill="#ffffff">El contexto</text>
    <text x="540" y="216" font-family="Inter,Arial,sans-serif" font-size="58" font-weight="800" letter-spacing="-2" fill="#ffffff">en Chile</text>
    <rect x="540" y="248" width="360" height="5" rx="3" fill="url(#rule)"/>
    <text x="540" y="318" font-family="Inter,Arial,sans-serif" font-size="25" font-weight="500" fill="#d2d4e2">
      <tspan x="540" dy="0">Entre las sustancias utilizadas</tspan>
      <tspan x="540" dy="34">comúnmente se encuentran:</tspan>
    </text>
    ${list}
  </g>

  <g opacity=".7">
    <circle cx="505" cy="382" r="5" fill="#ff8b50"/>
    <circle cx="521" cy="396" r="3" fill="#50e6f0"/>
    <circle cx="488" cy="400" r="3" fill="#b98cff"/>
    <path d="M488 400 C520 438 535 452 568 436" fill="none" stroke="#b98cff" stroke-opacity=".35" stroke-width="2"/>
  </g>

  <circle cx="1000" cy="1314" r="7" fill="#ff6d88"/>
  <circle cx="1025" cy="1314" r="7" fill="#50e6f0"/>
  <circle cx="1050" cy="1314" r="7" fill="#ffbd4a"/>
</svg>
`

fs.writeFileSync(svgPath, svg, "utf8")
console.log(JSON.stringify({ svg: svgPath, iconCount: icons.length, iconDir }, null, 2))
