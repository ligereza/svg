import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { rasterizeSvg } from "../src/tools/svg.mjs"

test("svg.rasterize creates a PNG fallback for complex SVG assets", async () => {
  const directory = path.join(process.cwd(), "jobs", `svg-rasterize-test-${Date.now()}`)
  const output = path.join(directory, "output", "fallback.png")
  const source = path.join(process.cwd(), "jobs", "document-to-animated-post-20260817092516-8tw9g", "output", "parts", "01-p-gina-1.svg")
  try {
    const result = await rasterizeSvg(source, output, { width: 512, overwrite: true })
    assert.equal(result.png, output)
    const bytes = await fs.readFile(output)
    assert.equal(bytes.subarray(0, 8).toString("hex"), "89504e470d0a1a0a")
  } finally {
    await fs.rm(directory, { recursive: true, force: true })
  }
})
