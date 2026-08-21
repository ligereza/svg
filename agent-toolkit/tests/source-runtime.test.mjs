import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { effectRetrySimulation, rxjsEventTimeline, stdlibStatistics, threeScenePreview } from "../src/tools/source-runtime.mjs"
import { TOOLKIT_ROOT } from "../src/utils.mjs"

test("three.js local runtime creates a browser preview from a declarative scene", async () => {
  const output = path.join(TOOLKIT_ROOT, "jobs", "test-source-runtime", "output", "scene.html")
  const result = await threeScenePreview({ canvas: { width: 320, height: 240 }, objects: [{ name: "icon", type: "plane", size: [1, 1], color: "#ff00aa" }] }, output, { overwrite: true })
  assert.equal(result.engine, "three-local")
  assert.equal(result.objectCount, 1)
  assert.match(await fs.readFile(result.html, "utf8"), /three\.module\.js/)
  assert.ok((await fs.stat(result.threeModule)).size > 100000)
})

test("stdlib local runtime computes statistics", async () => {
  const result = await stdlibStatistics([1, 2, 3, 4], { correction: 0 })
  assert.equal(result.engine, "stdlib-local")
  assert.equal(result.mean, 2.5)
  assert.ok(Math.abs(result.variance - 1.25) < 0.00001)
})

test("RxJS local runtime consumes an auditable event timeline", async () => {
  const result = await rxjsEventTimeline([{ type: "layout" }, { type: "render" }, { type: "render" }])
  assert.equal(result.engine, "rxjs-local")
  assert.equal(result.count, 3)
  assert.deepEqual(result.byType, { layout: 1, render: 2 })
  assert.equal(result.completed, true)
})

test("Effect local runtime retries a bounded failing operation", async () => {
  const result = await effectRetrySimulation({ failuresBeforeSuccess: 2, maxRetries: 2, value: "render" })
  assert.equal(result.engine, "effect-local")
  assert.equal(result.status, "succeeded")
  assert.equal(result.attempts, 3)
  assert.equal(result.value.value, "render")
})
