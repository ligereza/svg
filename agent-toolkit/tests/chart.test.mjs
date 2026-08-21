import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { animateChart, barChart } from "../src/tools/chart.mjs"
import { TOOLKIT_ROOT } from "../src/utils.mjs"

test("data chart and animation workflow", async () => {
  const directory = path.join(TOOLKIT_ROOT, "jobs", "_test-chart", "output")
  const input = path.join(directory, "data.json")
  const chart = path.join(directory, "chart.svg")
  const animated = path.join(directory, "chart-animated.svg")
  await fs.rm(path.join(TOOLKIT_ROOT, "jobs", "_test-chart"), { recursive: true, force: true })
  await fs.mkdir(directory, { recursive: true })
  await fs.writeFile(input, JSON.stringify([{ label: "A", value: 2 }, { label: "B", value: 5 }]))
  await barChart(input, chart, { x: "label", y: "value" })
  await animateChart(chart, animated, 600)
  const output = await fs.readFile(animated, "utf8")
  assert.match(output, /agent-chart-bars/)
  assert.match(output, /chart-bar-animated/)
  assert.match(output, /prefers-reduced-motion/)
  await fs.rm(path.join(TOOLKIT_ROOT, "jobs", "_test-chart"), { recursive: true, force: true })
})
