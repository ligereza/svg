import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { validateSvg } from "../src/tools/svg.mjs"
import { TOOLKIT_ROOT } from "../src/utils.mjs"

test("SVG validator reports missing accessibility metadata", async () => {
  const directory = path.join(TOOLKIT_ROOT, "jobs", "_test-accessibility", "output")
  const source = path.join(directory, "inaccessible.svg")
  await fs.mkdir(directory, { recursive: true })
  await fs.writeFile(source, '<svg xmlns="http://www.w3.org/2000/svg"><circle/></svg>')
  const result = await validateSvg(source)
  assert.equal(result.valid, true)
  assert.ok(result.warnings.includes("Missing accessible <title>"))
  assert.ok(result.warnings.includes("Missing accessible <desc>"))
  assert.ok(result.warnings.includes('SVG root should declare role="img"'))
  await fs.rm(path.join(TOOLKIT_ROOT, "jobs", "_test-accessibility"), { recursive: true, force: true })
})
