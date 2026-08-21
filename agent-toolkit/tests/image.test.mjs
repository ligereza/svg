import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { splitRaster } from "../src/tools/image.mjs"

test("image.split creates a reusable tile manifest with alpha-preserving PNGs", async () => {
  const directory = path.join(process.cwd(), "jobs", `image-split-test-${Date.now()}`)
  const output = path.join(directory, "output", "tiles.json")
  const source = path.join(process.cwd(), "projects", "chemsex", "generated", "slide-06-care-open-palette-v4.png")
  try {
    const result = await splitRaster(source, output, { rows: 2, columns: 2, overlap: 2, overwrite: true })
    assert.equal(result.manifest.assets.length, 4)
    assert.equal(result.manifest.assets[0].alpha, true)
    assert.deepEqual(result.manifest.assets.map((asset) => asset.slideIndex), [1, 2, 3, 4])
    for (const file of result.manifest.files) assert.equal((await fs.stat(file)).isFile(), true)
  } finally {
    await fs.rm(directory, { recursive: true, force: true })
  }
})
