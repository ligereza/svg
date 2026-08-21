import fs from "node:fs/promises"
import path from "node:path"

const [input, output] = process.argv.slice(2)
if (!input || !output) throw new Error("Usage: node scripts/improve-ascii-animation.mjs INPUT.svg OUTPUT.svg")

let svg = await fs.readFile(input, "utf8")

svg = svg.replace(/(<svg\b[^>]*?)aria-labelledby="title desc"/i, '$1aria-labelledby="svg-title svg-desc"')
if (!/<title\b/i.test(svg)) {
  svg = svg.replace(
    /(<svg\b[^>]*>)/i,
    '$1<title id="svg-title">ASCII README vessel in motion</title><desc id="svg-desc">A 30-frame animated ASCII vessel with a purple liquid core and luminous highlights.</desc>',
  )
}

svg = svg.replace(
  /\.frame\{opacity:0;animation:showFrame 9s step-end infinite\}/,
  ".frame{opacity:0;animation:showFrame 9s linear infinite;will-change:opacity}",
)
svg = svg.replace(
  /\.liquid\{fill:#c084fc;stroke:#9333ea;stroke-width:\.32;paint-order:stroke;opacity:\.94\}/,
  ".liquid{fill:#c084fc;stroke:#9333ea;stroke-width:.32;paint-order:stroke;opacity:.94;animation:liquidBreath 2.4s ease-in-out infinite alternate}",
)
svg = svg.replace(
  "@keyframes showFrame{0%,3.333%{opacity:1}3.334%,100%{opacity:0}}",
  "@keyframes showFrame{0%{opacity:0}0.667%{opacity:1}2.666%{opacity:1}3.333%,100%{opacity:0}}@keyframes liquidBreath{0%{opacity:.82}100%{opacity:1}}",
)
svg = svg.replace(
  /\.liquid-glint\{animation:none!important\}/g,
  ".liquid-glint,.liquid{animation:none!important}",
)

await fs.mkdir(path.dirname(output), { recursive: true })
await fs.writeFile(output, svg, "utf8")
console.log(JSON.stringify({ input, output, improvements: ["crossfade-between-frames", "liquid-breath", "reduced-motion-liquid", "accessible-title-description"] }, null, 2))
