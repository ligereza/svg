import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { execFile } from "node:child_process"
import { promisify } from "node:util"
import { removeIconBackground } from "../src/tools/image.mjs"

const execFileAsync = promisify(execFile)

function checkerboardPpm(width = 128, height = 128, cell = 16) {
  const pixels = Buffer.alloc(width * height * 3)
  const put = (x, y, color) => {
    const offset = (y * width + x) * 3
    pixels[offset] = color[0]
    pixels[offset + 1] = color[1]
    pixels[offset + 2] = color[2]
  }
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      put(x, y, ((Math.floor(x / cell) + Math.floor(y / cell)) % 2 === 0) ? [246, 246, 246] : [218, 218, 218])
    }
  }
  // This white/cream detail has a checkerboard-like luminance, but is part
  // of the dark icon. A global bright/neutral color key would remove it.
  for (let y = 28; y < 104; y += 1) {
    for (let x = 30; x < 100; x += 1) put(x, y, [19, 43, 58])
  }
  for (let y = 44; y < 88; y += 1) {
    for (let x = 44; x < 66; x += 1) put(x, y, [32, 126, 144])
  }
  for (let y = 55; y < 66; y += 1) {
    for (let x = 70; x < 88; x += 1) put(x, y, [246, 238, 214])
  }
  return Buffer.concat([Buffer.from(`P6\n${width} ${height}\n255\n`, "ascii"), pixels])
}

async function alphaAt(imagePath, x, y) {
  const script = "from PIL import Image; import sys; print(Image.open(sys.argv[1]).convert('RGBA').getpixel((int(sys.argv[2]), int(sys.argv[3])))[3])"
  const { stdout } = await execFileAsync(process.env.PYTHON_EXE || "python", ["-c", script, imagePath, String(x), String(y)])
  return Number(stdout.trim())
}

test("image.remove-background uses structural checkerboard seeds and preserves bright artwork", async () => {
  const directory = path.join(process.cwd(), "jobs", `icon-background-test-${Date.now()}`)
  const input = path.join(directory, "source.ppm")
  const output = path.join(directory, "output", "manifest.json")
  try {
    await fs.mkdir(directory, { recursive: true })
    await fs.writeFile(input, checkerboardPpm())
    const result = await removeIconBackground({ input, output, prefix: "fixture", padding: 128, overwrite: true })
    const asset = result.manifest.assets[0]
    assert.equal(result.manifest.assets.length, 1)
    assert.equal(asset.alpha, true)
    assert.equal(asset.background.mode, "checkerboard-grabcut")
    assert.ok(asset.background.grabcut.certainBackgroundPixels > 0)
    assert.ok(asset.background.grabcut.backgroundPixels > 0)
    assert.equal(await alphaAt(result.manifest.files[0], 2, 2), 0)
    assert.equal(await alphaAt(result.manifest.files[0], 78, 60), 255)
  } finally {
    await fs.rm(directory, { recursive: true, force: true })
  }
})
