import test from "node:test"
import assert from "node:assert/strict"
import fs from "node:fs/promises"
import path from "node:path"
import { runTool } from "../src/dispatcher.mjs"
import { TOOLKIT_ROOT } from "../src/utils.mjs"

const SOURCE = path.join(TOOLKIT_ROOT, "projects", "chemsex", "generated", "slide-08-close-flat-v6.png")

test("photoshop.separate-objects stages source and queues deterministic regions", async () => {
  const queued = await runTool("photoshop.separate-objects", {
    input: SOURCE,
    mode: "regions",
    objects: [{ name: "network", bounds: { left: 10, top: 20, right: 200, bottom: 300 } }],
    output: "separated/manifest.json",
    psdOutput: "separated/objects.psd",
  })
  assert.equal(queued.result.status, "queued")
  const command = JSON.parse(await fs.readFile(queued.result.command, "utf8"))
  assert.equal(command.app, "photoshop")
  assert.equal(command.operation, "separate-objects")
  assert.equal(command.options.mode, "regions")
  assert.equal(command.options.objects[0].name, "network")
  assert.equal(command.input.startsWith(queued.directory), true)
  await fs.access(command.input)
})
