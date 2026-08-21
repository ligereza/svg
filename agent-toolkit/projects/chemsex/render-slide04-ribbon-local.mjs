import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

const here = path.dirname(fileURLToPath(import.meta.url))
const iconDir = path.resolve(here, "../../../rd_database_complete/assets/generated_icons")
const backgroundPath = "C:\\Users\\issvk\\.codex\\generated_images\\01a01361-7f6d-76b0-b1b1-f4c1c81197fe\\exec-cdd86596-df6c-49d2-a1a4-cec1d19e42ca.png"
const outputDir = path.join(here, "generated", "slide-04-substances")
const svgPath = path.join(outputDir, "slide-04-ribbon-local.svg")
fs.mkdirSync(outputDir, { recursive: true })

const pngUri = (filename) => `data:image/png;base64,${fs.readFileSync(filename).toString("base64")}`
const iconUri = (filename) => pngUri(path.join(iconDir, filename))
const bgUri = pngUri(backgroundPath)

const icon = ({ file, x, y, size, rotation, accent, opacity = 1 }) => {
  const cx = x + size / 2
  const cy = y + size / 2
  return `
    <g transform="rotate(${rotation} ${cx} ${cy})" opacity="${opacity}">
      <circle cx="${cx}" cy="${cy}" r="${size * .4}" fill="${accent}" opacity=".18" filter="url(#softGlow)"/>
      <image href="${iconUri(file)}" x="${x}" y="${y}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet" filter="url(#iconShadow)"/>
    </g>`
}

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1440" viewBox="0 0 1080 1440" role="img" aria-labelledby="title desc">
  <title id="title">Composición de cinta escultórica sin texto para la lámina 4 de Chemsex</title>
  <desc id="desc">Ocho iconos editoriales integrados en una cinta translúcida y un campo oscuro libre para texto.</desc>
  <defs>
    <filter id="softGlow"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="iconShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="0" dy="12" stdDeviation="9" flood-color="#02030b" flood-opacity=".85"/>
    </filter>
  </defs>

  <image href="${bgUri}" x="0" y="0" width="1080" height="1440" preserveAspectRatio="none"/>

  <!-- The eight exact icons are embedded in different folds of one continuous form. -->
  ${icon({ file: "amphetamine.png", x: 46, y: 74, size: 192, rotation: -17, accent: "#ffb735" })}
  ${icon({ file: "mdma.png", x: 292, y: 138, size: 158, rotation: 13, accent: "#ff638f" })}
  ${icon({ file: "cannabis.png", x: 38, y: 386, size: 188, rotation: -24, accent: "#9bd94d" })}
  ${icon({ file: "alkyl_nitrites.png", x: 326, y: 404, size: 142, rotation: 18, accent: "#54dce9" })}
  ${icon({ file: "cocaine.png", x: 88, y: 620, size: 190, rotation: -9, accent: "#f1e2c2" })}
  ${icon({ file: "ketamine.png", x: 380, y: 690, size: 146, rotation: 11, accent: "#7eaaff" })}
  ${icon({ file: "methamphetamine.png", x: 108, y: 900, size: 198, rotation: -14, accent: "#2bc9ef" })}
  ${icon({ file: "ghb_gbl.png", x: 392, y: 1034, size: 150, rotation: 9, accent: "#8bbcff" })}

  <!-- No text or labels: the right side remains the editable copy field. -->
</svg>
`

fs.writeFileSync(svgPath, svg, "utf8")
console.log(JSON.stringify({ svg: svgPath, iconCount: 8, textElements: 0, background: backgroundPath }, null, 2))
