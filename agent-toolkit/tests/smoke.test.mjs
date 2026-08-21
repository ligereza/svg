import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { createSvg, animateSvg, validateSvg, previewSvg } from "../src/tools/svg.mjs"
import { TOOLKIT_ROOT } from "../src/utils.mjs"

test("SVG create, animate, validate and preview workflow", async () => {
  const directory = path.join(TOOLKIT_ROOT, "jobs", "_test-smoke", "output")
  await fs.rm(path.join(TOOLKIT_ROOT, "jobs", "_test-smoke"), { recursive: true, force: true })
  await fs.mkdir(directory, { recursive: true })
  const source = path.join(directory, "source.svg")
  const animated = path.join(directory, "animated.svg")
  const preview = path.join(directory, "preview.html")
  await createSvg({ width: 320, height: 180, background: "#111827", elements: [{ type: "circle", cx: 160, cy: 90, r: 30, attrs: { fill: "#7dd3fc" } }] }, source)
  await animateSvg(source, animated, "pulse", 500)
  const validation = await validateSvg(animated)
  await previewSvg(animated, preview)
  assert.equal(validation.valid, true)
  assert.deepEqual(validation.warnings, [])
  assert.match(await fs.readFile(animated, "utf8"), /aria-labelledby="svg-title svg-desc"/)
  assert.match(await fs.readFile(animated, "utf8"), /@keyframes agent-pulse/)
  assert.match(await fs.readFile(preview, "utf8"), /<svg/)
  await fs.rm(path.join(TOOLKIT_ROOT, "jobs", "_test-smoke"), { recursive: true, force: true })
})
