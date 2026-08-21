import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { thiNgSvg } from "../src/tools/source-runtime.mjs"
import { TOOLKIT_ROOT } from "../src/utils.mjs"

test("thi.ng geom source generates editable SVG shapes", async () => {
  const output = path.join(TOOLKIT_ROOT, "jobs", "test-source-runtime", "output", "thi-ng.svg")
  const result = await thiNgSvg({ width: 120, height: 90, shapes: [{ type: "rect", x: 8, y: 10, width: 30, height: 20, fill: "#f00" }, { type: "circle", x: 80, y: 45, radius: 12, fill: "#0ff" }] }, output, { overwrite: true })
  const svg = await fs.readFile(result.svg, "utf8")
  assert.equal(result.engine, "thi-ng-geom-local")
  assert.equal(result.shapes, 2)
  assert.match(svg, /<rect/)
  assert.match(svg, /<circle/)
})
