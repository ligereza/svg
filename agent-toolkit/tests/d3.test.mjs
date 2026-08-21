import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { d3BarChart } from "../src/tools/d3.mjs"
import { TOOLKIT_ROOT } from "../src/utils.mjs"

test("D3 local source generates a scaled SVG chart", async () => {
  const input = path.join(TOOLKIT_ROOT, "tests", "fixtures", "d3-chart.json")
  const output = path.join(TOOLKIT_ROOT, "jobs", "test-d3", "output", "chart.svg")
  const result = await d3BarChart(input, output, { overwrite: true, x: "label", y: "value" })
  const svg = await fs.readFile(output, "utf8")
  assert.equal(result.engine, "d3-local")
  assert.equal(result.rows, 3)
  assert.match(svg, /data-value="12"/)
  assert.match(svg, /D3 bar chart/)
})
