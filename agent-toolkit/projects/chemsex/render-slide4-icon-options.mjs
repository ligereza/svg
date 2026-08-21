import fs from "node:fs/promises"
import path from "node:path"
import { rasterizeSvg } from "../../src/tools/svg.mjs"

const root = path.resolve("C:/IA/svg/agent-toolkit")
const outDir = path.join(root, "projects/chemsex/generated/slide4-icon-options")
const canvas = { width: 1440, height: 1980 }

const rows = [
  {
    label: "Éxtasis (pasti o pilas)",
    status: "forma genérica",
    options: [
      ["Pastilla Bioicons · CC0", "projects/chemsex/libraries/bioicons/static/icons/cc-0/Human_physiology/Marcel_Tisch/pill_blue.svg", "#f3b83f"],
      ["Tableta Bioicons · CC BY 3.0", "projects/chemsex/libraries/bioicons/static/icons/cc-by-3.0/Human_physiology/Servier/drug-tablet-1.svg", "#5ec8d7"],
      ["Pastilla Health Icons · CC0", "projects/chemsex/libraries/healthicons/public/icons/svg/outline/medications/pill-1.svg", "#ff755b"]
    ]
  },
  {
    label: "MDMA",
    status: "forma genérica; no ícono MDMA exacto",
    options: [
      ["Grupo de drogas Bioicons · CC0", "projects/chemsex/libraries/bioicons/static/icons/cc-0/Human_physiology/Marcel_Tisch/drugs.svg", "#f3b83f"],
      ["Cápsula Bioicons · CC BY 3.0", "projects/chemsex/libraries/bioicons/static/icons/cc-by-3.0/Human_physiology/Servier/drug-capsule-1.svg", "#5ec8d7"],
      ["Pastilla material · Apache-2.0", "projects/chemsex/assets/iconify-material-symbols-pill.svg", "#ff755b"]
    ]
  },
  {
    label: "Marihuana",
    status: "símbolo específico disponible",
    options: [
      ["Cannabis Health Icons · CC0", "projects/chemsex/libraries/healthicons/public/icons/svg/outline/symbols/cannabis.svg", "#b8d83f"],
      ["Cannabis material · Apache-2.0", "projects/chemsex/assets/iconify-material-symbols-cannabis.svg", "#5ec8d7"],
      ["Cannabis Health Icons lleno · CC0", "projects/chemsex/libraries/healthicons/public/icons/svg/filled/symbols/cannabis.svg", "#ff755b"]
    ]
  },
  {
    label: "Popper",
    status: "botella/gota; no ícono popper exacto",
    options: [
      ["Botella Bioicons · CC BY 3.0", "projects/chemsex/libraries/bioicons/static/icons/cc-by-3.0/Human_physiology/Servier/bottle-drug.svg", "#f3b83f"],
      ["Gota MDI · Apache-2.0", "projects/chemsex/assets/iconify-mdi-drop.svg", "#5ec8d7"],
      ["Botella Tabler · MIT", "projects/chemsex/assets/iconify-tabler-bottle.svg", "#ff755b"]
    ]
  },
  {
    label: "Cocaína",
    status: "polvo; no ícono cocaína exacto",
    options: [
      ["Polvo Icon Park · Apache-2.0", "projects/chemsex/assets/iconify-icon-park-outline-powder.svg", "#f3b83f"],
      ["Gránulos en frasco Bioicons · CC BY 3.0", "projects/chemsex/libraries/bioicons/static/icons/cc-by-3.0/Human_physiology/Servier/drug-granule-bottle-open.svg", "#5ec8d7"],
      ["Molécula MDI · Apache-2.0", "projects/chemsex/assets/iconify-mdi-molecule.svg", "#ff755b"]
    ]
  },
  {
    label: "Ketamina",
    status: "molécula/botella; no ícono ketamina exacto",
    options: [
      ["Molécula MDI · Apache-2.0", "projects/chemsex/assets/iconify-mdi-molecule.svg", "#f3b83f"],
      ["Botella química Bioicons · CC BY 4.0", "projects/chemsex/libraries/bioicons/static/icons/cc-by-4.0/Chemistry/DBCLS/Reagent_bottle.svg", "#5ec8d7"],
      ["Botella médica Health Icons · CC0", "projects/chemsex/libraries/healthicons/public/icons/svg/filled/devices/medicine-bottle.svg", "#ff755b"]
    ]
  },
  {
    label: "Metanfetamina (cristal)",
    status: "cristal/molécula; no ícono metanfetamina exacto",
    options: [
      ["Drogas genéricas Bioicons · CC0", "projects/chemsex/libraries/bioicons/static/icons/cc-0/Human_physiology/Marcel_Tisch/drugs.svg", "#f3b83f"],
      ["Molécula MDI · Apache-2.0", "projects/chemsex/assets/iconify-mdi-molecule.svg", "#5ec8d7"],
      ["Frasco químico Bioicons · CC BY 4.0", "projects/chemsex/libraries/bioicons/static/icons/cc-by-4.0/Chemistry/DBCLS/Reagent_bottle-brown.svg", "#ff755b"]
    ]
  },
  {
    label: "GHB",
    status: "gota/botella; no ícono GHB exacto",
    options: [
      ["Gota MDI · Apache-2.0", "projects/chemsex/assets/iconify-mdi-drop.svg", "#f3b83f"],
      ["Gotas y frascos Bioicons · CC0", "projects/chemsex/libraries/bioicons/static/icons/cc-0/Lab_apparatus/OpenClipart/dropper-bottles.svg", "#5ec8d7"],
      ["Botella médica Health Icons · CC0", "projects/chemsex/libraries/healthicons/public/icons/svg/filled/devices/medicine-bottle.svg", "#ff755b"]
    ]
  }
]

const esc = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;")

async function readAsset(relative) {
  const source = path.join(root, relative)
  const svg = await fs.readFile(source, "utf8")
  const viewBox = svg.match(/viewBox=["']([^"']+)["']/i)?.[1]?.trim().split(/[ ,]+/).map(Number)
  const vb = viewBox?.length === 4 ? viewBox : [0, 0, 24, 24]
  const inner = svg.replace(/<\?xml[^>]*>/gi, "").replace(/<!DOCTYPE[^>]*>/gi, "").replace(/<svg\b[^>]*>/i, "").replace(/<\/svg>/i, "")
  return { inner, vb }
}

function fit(vb, x, y, w, h) {
  const scale = Math.min(w / vb[2], h / vb[3])
  const tx = x + (w - vb[2] * scale) / 2 - vb[0] * scale
  const ty = y + (h - vb[3] * scale) / 2 - vb[1] * scale
  return `translate(${tx.toFixed(2)} ${ty.toFixed(2)}) scale(${scale.toFixed(5)})`
}

async function build() {
  await fs.mkdir(outDir, { recursive: true })
  const parts = []
  parts.push(`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${canvas.width}" height="${canvas.height}" viewBox="0 0 ${canvas.width} ${canvas.height}" role="img"><title>Opciones de íconos para la lámina 4</title><desc>Ocho sustancias con tres alternativas de representación visual por sustancia.</desc>`)
  parts.push(`<rect width="100%" height="100%" fill="#07113d"/>`)
  parts.push(`<rect x="36" y="32" width="1368" height="124" rx="28" fill="#101d5b" stroke="#31437f" stroke-width="2"/>`)
  parts.push(`<text x="72" y="84" fill="#fff7df" font-family="Arial, sans-serif" font-size="34" font-weight="700">LÁMINA 4 · OPCIONES DE ÍCONOS</text>`)
  parts.push(`<text x="72" y="126" fill="#b7c5ee" font-family="Arial, sans-serif" font-size="20">Cada fila corresponde a una sustancia del texto. Las columnas son alternativas, no afirmaciones de identidad química.</text>`)

  const startY = 180
  const rowH = 216
  const labelW = 340
  const cardW = 330
  const cardGap = 18
  const iconW = 118
  const iconH = 118
  for (let row = 0; row < rows.length; row += 1) {
    const item = rows[row]
    const y = startY + row * rowH
    parts.push(`<rect x="36" y="${y}" width="1368" height="196" rx="24" fill="${row % 2 ? "#0b1748" : "#0e1b52"}" stroke="#263774" stroke-width="2"/>`)
    parts.push(`<text x="66" y="${y + 56}" fill="#fff7df" font-family="Arial, sans-serif" font-size="25" font-weight="700">${esc(item.label)}</text>`)
    parts.push(`<text x="66" y="${y + 92}" fill="#8ee8ef" font-family="Arial, sans-serif" font-size="16">${esc(item.status)}</text>`)
    for (let col = 0; col < item.options.length; col += 1) {
      const [name, relative, accent] = item.options[col]
      const x = 386 + col * (cardW + cardGap)
      const asset = await readAsset(relative)
      parts.push(`<rect x="${x}" y="${y + 18}" width="${cardW}" height="160" rx="18" fill="#f8f5ee"/>`)
      parts.push(`<circle cx="${x + 58}" cy="${y + 80}" r="48" fill="${accent}" opacity="0.22"/>`)
      parts.push(`<g transform="${fit(asset.vb, x + 10, y + 22, iconW, iconH)}" color="#111a3c" fill="#111a3c" stroke="#111a3c">${asset.inner}</g>`)
      parts.push(`<text x="${x + 142}" y="${y + 58}" fill="#111a3c" font-family="Arial, sans-serif" font-size="15" font-weight="700">Opción ${col + 1}</text>`)
      parts.push(`<text x="${x + 142}" y="${y + 84}" fill="#253057" font-family="Arial, sans-serif" font-size="14">${esc(name)}</text>`)
    }
  }
  parts.push(`<text x="72" y="${canvas.height - 30}" fill="#8fa1d3" font-family="Arial, sans-serif" font-size="16">Fuente: bibliotecas locales Bioicons, Health Icons y assets Iconify previamente descargados. La licencia se conserva por archivo.</text>`)
  parts.push("</svg>")
  const svgPath = path.join(outDir, "slide-04-icon-options.svg")
  const pngPath = path.join(outDir, "slide-04-icon-options.png")
  await fs.writeFile(svgPath, parts.join("\n"), "utf8")
  await rasterizeSvg(svgPath, pngPath, { overwrite: true, width: canvas.width, background: "#07113d" })
  console.log(JSON.stringify({ svg: svgPath, png: pngPath, rows: rows.length, options: rows.length * 3 }, null, 2))
}

await build()
