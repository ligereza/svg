import test from "node:test"
import assert from "node:assert/strict"
import { normalizeDesign } from "../src/tools/design.mjs"
import { estimateTextMetrics, planLayouts, scoreLayoutCandidate, semanticVector, VECTOR_AXES } from "../src/tools/layout.mjs"

const design = normalizeDesign({ preset: "instagram-portrait" })

function inside(box) {
  return box.x >= 0 && box.y >= 0 && box.width > 0 && box.height > 0 && box.x + box.width <= 1 && box.y + box.height <= 1
}

test("text metrics expose real copy load and overflow risk", () => {
  const short = estimateTextMetrics({ title: "Cuidado", text: "Hidratación y descanso.", typography: design.typography, width: 720, height: 480 })
  const long = estimateTextMetrics({ title: "Cómo cuidarnos", text: "Una recomendación extensa sobre hidratación, descanso, consentimiento, comunicación, pausas y pedir ayuda cuando sea necesario. ".repeat(8), typography: design.typography, width: 360, height: 220 })
  assert.ok(short.wordCount > 0)
  assert.ok(long.bodyChars > short.bodyChars)
  assert.ok(long.estimatedLines > short.estimatedLines)
  assert.equal(typeof long.overflow, "boolean")
  assert.ok(long.recommendedSummarySize <= design.typography.summarySize)
})

test("semantic layouts vary by theme and preserve safe bounds", () => {
  const parts = [
    { title: "CHEMSEX", sourceText: "Orgullo es cuidarnos en comunidad.", keywords: ["comunidad"] },
    { title: "¿Qué es el chemsex?", sourceText: "El chemsex se refiere al uso intencional de sustancias para facilitar, intensificar o prolongar experiencias sexuales.", keywords: ["sustancias"] },
    { title: "Contexto en Chile", sourceText: "Datos y contexto social para comprender el fenómeno.", keywords: ["contexto", "chile"] },
    { title: "Cómo cuidarnos", sourceText: "Hidratación, descanso, consentimiento y comunicación.", keywords: ["cuidado"] },
    { title: "Interacciones más riesgosas", sourceText: "Mezclar sustancias puede aumentar los riesgos.", keywords: ["interacciones"] },
    { title: "Cierre", sourceText: "La comunidad y el apoyo importan.", keywords: ["comunidad"] },
  ]
  const planned = planLayouts(parts, design)
  assert.deepEqual(planned.map((part) => part.theme), ["cover", "definition", "context", "care", "interactions", "close"])
  assert.ok(new Set(planned.map((part) => part.layout.variant)).size >= 4)
  for (const part of planned) {
    assert.ok(inside(part.layout.text), `${part.title} text box outside canvas`)
    assert.ok(inside(part.layout.illustration), `${part.title} illustration box outside canvas`)
    assert.ok(part.semanticTags.length > 0)
    assert.equal(typeof part.textMetrics.bodyChars, "number")
  }
})

test("manual composition remains available", () => {
  const manual = normalizeDesign({
    preset: "instagram-portrait",
    autoLayout: false,
    layout: {
      mode: "manual",
      text: { x: 0.1, y: 0.1, width: 0.3, height: 0.3 },
      illustration: { x: 0.5, y: 0.2, width: 0.4, height: 0.6 },
    },
  })
  const [part] = planLayouts([{ title: "Manual", sourceText: "Texto exacto", keywords: [] }], manual)
  assert.equal(part.layout.mode, "manual")
  assert.deepEqual(part.layout.text, manual.layout.text)
  assert.deepEqual(part.layout.illustration, manual.layout.illustration)
})

test("custom canvas preset keeps user proportions", () => {
  const custom = normalizeDesign({
    preset: "custom",
    canvas: { width: 1440, height: 1800 },
    margins: { top: 120, right: 100, bottom: 140, left: 100 },
  })
  assert.equal(custom.preset, "custom")
  assert.deepEqual(custom.canvas, { width: 1440, height: 1800 })
  assert.deepEqual(custom.margins, { top: 120, right: 100, bottom: 140, left: 100 })
})

test("Chemsex portrait preset is fixed at 1080x1440", () => {
  const chemsex = normalizeDesign({ preset: "chemsex-portrait" })
  assert.deepEqual(chemsex.canvas, { width: 1080, height: 1440 })
})

test("Chemsex layout selection exposes auditable vectors and scores", () => {
  const planned = planLayouts([
    { title: "Interacciones más riesgosas", sourceText: "Mezclar sustancias puede aumentar el riesgo.", keywords: ["interacciones"] },
  ], design)[0]
  assert.equal(planned.theme, "interactions")
  assert.equal(planned.contentVector.length, VECTOR_AXES.length)
  assert.equal(planned.layoutVector.length, VECTOR_AXES.length)
  assert.equal(typeof planned.layoutScore, "number")
  assert.ok(planned.layoutScore > 0)
  assert.ok(scoreLayoutCandidate({ theme: "interactions", variant: "diagonal", load: 0.8, metrics: { density: 0.5 } }) > scoreLayoutCandidate({ theme: "interactions", variant: "full-bleed-art", load: 0.8, metrics: { density: 0.5 } }))
  assert.equal(semanticVector("interactions", 0.8).at(-1), 0.8)
})
