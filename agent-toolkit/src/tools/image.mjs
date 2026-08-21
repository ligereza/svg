import fs from "node:fs/promises"
import path from "node:path"
import { spawn } from "node:child_process"
import { fileURLToPath } from "node:url"
import { ensureDir, resolveInput, resolveOutput } from "../utils.mjs"

const script = fileURLToPath(new URL("../../adapters/image/split.py", import.meta.url))

export async function splitRaster(input, output, options = {}) {
  const inputPath = resolveInput(input)
  const outputPath = resolveOutput(output, options)
  await ensureDir(path.dirname(outputPath))
  const python = process.env.PYTHON_EXE || "python"
  const args = [
    script,
    "--input", inputPath,
    "--output", outputPath,
    "--rows", String(options.rows || 1),
    "--columns", String(options.columns || 1),
    "--mode", String(options.mode || "grid"),
    "--overlap", String(options.overlap || 0),
    "--prefix", String(options.prefix || "tile"),
  ]
  return await new Promise((resolve, reject) => {
    const child = spawn(python, args, { cwd: path.dirname(script), windowsHide: true })
    let stdout = ""
    let stderr = ""
    child.stdout.on("data", (chunk) => { stdout += chunk })
    child.stderr.on("data", (chunk) => { stderr += chunk })
    child.on("error", (error) => reject(new Error(`Could not start Python: ${error.message}`)))
    child.on("close", async (code) => {
      if (code !== 0) return reject(new Error(`Image splitter exited with ${code}\n${stderr}`))
      try {
        const result = JSON.parse(stdout.trim().split(/\r?\n/).at(-1))
        const manifest = JSON.parse(await fs.readFile(outputPath, "utf8"))
        resolve({ ...result, manifest, output: outputPath, files: [outputPath, ...(manifest.files || [])] })
      } catch (error) {
        reject(new Error(`Image splitter returned invalid output: ${error.message}\n${stdout}`))
      }
    })
  })
}
