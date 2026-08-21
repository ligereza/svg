import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

const here = path.dirname(fileURLToPath(import.meta.url))
const iconDir = path.resolve(here, "../../../rd_database_complete/assets/generated_icons")
const outputDir = path.join(here, "generated", "slide-04-substances")
const svgPath = path.join(outputDir, "slide-04-composition-v2.svg")

fs.mkdirSync(outputDir, { recursive: true })

const dataUri = (filename) => `data:image/png;base64,${fs.readFileSync(path.join(iconDir, filename)).toString("base64")}`

const icon = ({ file, x, y, size, rotation, opacity = 1, accent, halo = 1 }) => {
  const image = dataUri(file)
  const cx = x + size / 2
  const cy = y + size / 2
  return `
    <g transform="rotate(${rotation} ${cx} ${cy})" opacity="${opacity}">
      <circle cx="${cx}" cy="${cy}" r="${size * 0.43 * halo}" fill="${accent}" opacity=".08" filter="url(#blur18)"/>
      <circle cx="${cx}" cy="${cy}" r="${size * 0.42 * halo}" fill="none" stroke="${accent}" stroke-opacity=".22" stroke-width="2" stroke-dasharray="5 13"/>
      <image href="${image}" x="${x}" y="${y}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet"/>
    </g>`
}

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440" role="img" aria-labelledby="title desc">
  <title id="title">Composición visual sin texto para la lámina 4 de Chemsex</title>
  <desc id="desc">Constelación editorial de ocho iconos visuales con un campo limpio reservado para texto editable.</desc>
  <defs>
    <radialGradient id="base" cx="18%" cy="42%" r="72%">
      <stop offset="0" stop-color="#342063"/>
      <stop offset=".44" stop-color="#111836"/>
      <stop offset="1" stop-color="#070913"/>
    </radialGradient>
    <radialGradient id="warm" cx="70%" cy="50%" r="60%">
      <stop offset="0" stop-color="#ff7f5b" stop-opacity=".31"/>
      <stop offset=".55" stop-color="#ad4d80" stop-opacity=".10"/>
      <stop offset="1" stop-color="#070913" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="violetCyan" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#a77dff"/>
      <stop offset=".48" stop-color="#53e5eb"/>
      <stop offset="1" stop-color="#ff8d58"/>
    </linearGradient>
    <filter id="blur18"><feGaussianBlur stdDeviation="18"/></filter>
    <filter id="blur70"><feGaussianBlur stdDeviation="70"/></filter>
    <pattern id="grain" width="48" height="48" patternUnits="userSpaceOnUse">
      <circle cx="5" cy="8" r="1" fill="#fff" opacity=".05"/>
      <circle cx="30" cy="23" r="1" fill="#fff" opacity=".035"/>
      <circle cx="42" cy="43" r="1" fill="#fff" opacity=".04"/>
      <path d="M12 35l5-2M34 7l5 2" stroke="#fff" stroke-opacity=".025"/>
    </pattern>
  </defs>

  <rect width="1080" height="1440" fill="#070913"/>
  <rect x="16" y="16" width="1048" height="1408" fill="url(#base)"/>
  <rect x="16" y="16" width="1048" height="1408" fill="url(#warm)"/>
  <ellipse cx="870" cy="735" rx="270" ry="470" fill="#ff6c73" opacity=".08" filter="url(#blur70)"/>
  <ellipse cx="235" cy="690" rx="270" ry="500" fill="#8e55ff" opacity=".13" filter="url(#blur70)"/>
  <rect x="16" y="16" width="1048" height="1408" fill="url(#grain)"/>

  <!-- Organic constellation lines: visual rhythm, not a rigid grid. -->
  <g fill="none" stroke-linecap="round">
    <path d="M52 230 C180 128 256 272 365 185 S492 142 575 235" stroke="#b279ff" stroke-opacity=".52" stroke-width="3"/>
    <path d="M52 575 C148 516 234 604 327 548 S474 498 550 568" stroke="#50e6ef" stroke-opacity=".48" stroke-width="3"/>
    <path d="M74 914 C176 838 244 962 346 876 S470 828 560 908" stroke="#ff8861" stroke-opacity=".44" stroke-width="3"/>
    <path d="M78 1245 C175 1165 254 1302 356 1207 S470 1178 530 1248" stroke="#6fdde7" stroke-opacity=".36" stroke-width="3"/>
    <path d="M536 248 C634 185 700 246 752 174" stroke="url(#violetCyan)" stroke-opacity=".28" stroke-width="2" stroke-dasharray="3 12"/>
    <path d="M552 1110 C650 1050 725 1140 820 1086" stroke="url(#violetCyan)" stroke-opacity=".22" stroke-width="2" stroke-dasharray="3 12"/>
  </g>

  <!-- Eight unique library icons, varied in scale and angle; every silhouette remains whole. -->
  ${icon({ file: "amphetamine.png", x: 36, y: 112, size: 248, rotation: -13, accent: "#ffb52e", halo: 1.1 })}
  ${icon({ file: "mdma.png", x: 284, y: 76, size: 204, rotation: 11, accent: "#ff668c", halo: .95 })}
  ${icon({ file: "cannabis.png", x: 14, y: 390, size: 236, rotation: -18, accent: "#9ad94e", halo: 1.05 })}
  ${icon({ file: "alkyl_nitrites.png", x: 282, y: 366, size: 204, rotation: 14, accent: "#51d9ee", halo: .94 })}
  ${icon({ file: "cocaine.png", x: 66, y: 650, size: 260, rotation: 8, accent: "#f2e3c1", halo: 1.12 })}
  ${icon({ file: "ketamine.png", x: 350, y: 654, size: 188, rotation: -12, accent: "#7eaaff", halo: .92 })}
  ${icon({ file: "methamphetamine.png", x: 28, y: 1004, size: 226, rotation: 12, accent: "#2ac9ef", halo: 1.02 })}
  ${icon({ file: "ghb_gbl.png", x: 328, y: 1018, size: 198, rotation: -9, accent: "#8bbcff", halo: .95 })}

  <!-- The right side remains intentionally quiet for the exact editable copy. -->
  <g opacity=".42" fill="none" stroke-linecap="round">
    <path d="M660 360 C760 280 870 364 1004 280" stroke="#b98cff" stroke-width="2" stroke-dasharray="2 16"/>
    <path d="M648 1080 C762 1008 858 1112 1018 1022" stroke="#ff9a69" stroke-width="2" stroke-dasharray="2 16"/>
    <circle cx="720" cy="350" r="7" fill="#50e6f0" stroke="none"/>
    <circle cx="944" cy="308" r="5" fill="#ff9a69" stroke="none"/>
    <circle cx="740" cy="1090" r="5" fill="#b98cff" stroke="none"/>
    <circle cx="970" cy="1035" r="7" fill="#ff668c" stroke="none"/>
  </g>

  <g opacity=".8">
    <circle cx="1010" cy="1285" r="8" fill="#ff668c"/>
    <circle cx="1035" cy="1285" r="8" fill="#50e6f0"/>
    <circle cx="1060" cy="1285" r="8" fill="#ffb52e"/>
  </g>
</svg>
`

fs.writeFileSync(svgPath, svg, "utf8")
console.log(JSON.stringify({ svg: svgPath, iconCount: 8, textElements: 0 }, null, 2))
