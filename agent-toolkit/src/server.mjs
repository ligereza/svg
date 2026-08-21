import http from "node:http"
import fs from "node:fs/promises"
import path from "node:path"
import { getJob, createJob } from "./jobs.mjs"
import { adobeStatus, enqueueAdobe } from "./adapters/adobe.mjs"
import { runTool, webToolList, WEB_RUN_TOOLS } from "./dispatcher.mjs"
import { assertAllowedInput, TOOLKIT_ROOT, readJson } from "./utils.mjs"
import { renderPlanner } from "./planner.mjs"
import { extractDocument } from "./tools/document.mjs"
import { integrationScriptingMap, integrationSources, validateIntegration } from "./tools/integration.mjs"

const registry = await readJson(path.join(TOOLKIT_ROOT, "registry.json"))
const config = await readJson(path.join(TOOLKIT_ROOT, "config.local.json")).catch(() => ({ server: {} }))
const host = process.env.AGENT_TOOLKIT_HOST || config.server?.host || "127.0.0.1"
const port = Number(process.env.AGENT_TOOLKIT_PORT || config.server?.port || 47921)
const token = process.env.AGENT_TOOLKIT_TOKEN || ""
const MAX_BODY_BYTES = 2_000_000
if (!token && !["127.0.0.1", "localhost", "::1"].includes(host)) {
  throw new Error("AGENT_TOOLKIT_TOKEN is required when the bridge is not bound to loopback")
}
const corsOrigins = new Set(
  (process.env.AGENT_TOOLKIT_CORS_ORIGINS || "")
    .split(",")
    .map((origin) => origin.trim())
    .filter(Boolean),
)

const agentCard = {
  name: "Agent Toolkit Local Bridge",
  version: "0.1.0",
  description: "Local allowlisted orchestrator for SVG, charts, Blender and Adobe job envelopes.",
  authentication: token ? "Bearer token" : "localhost-only; bearer token not configured",
  safety: {
    localhostOnlyByDefault: true,
    bearerRequiredForNonLoopback: true,
    maxBodyBytes: MAX_BODY_BYTES,
    arbitraryShell: false,
    outputOverwrite: false,
  },
  tools: registry.tools.map(({ id, description, status, input, output }) => ({ id, description, status, input, output })),
  webTools: webToolList(),
  workflows: ["workflow.image-to-svg-preview", "workflow.image-to-svg-blender-illustrator"],
  integration: {
    inventory: "integration.sources",
    scriptingMap: "integration.scripting-map",
    validation: "integration.validate",
    guide: "INTEGRATION-GUIDE.md",
  },
  adobeOperations: {
    photoshop: ["import-svg", "separate-objects"],
    illustrator: ["import-svg"],
    "after-effects": ["import-svg"],
    premiere: ["import-media", "create-sequence", "export-sequence"],
  },
}

const openApi = {
  openapi: "3.1.0",
  info: { title: "Agent Toolkit Local Bridge", version: "0.1.0" },
  servers: [{ url: `http://${host}:${port}` }],
  security: [{ bearerAuth: [] }],
  components: { securitySchemes: { bearerAuth: { type: "http", scheme: "bearer" } } },
  paths: {
    "/health": { get: { operationId: "health", responses: { "200": { description: "Bridge health" } } } },
    "/capabilities": { get: { operationId: "capabilities", responses: { "200": { description: "Tool registry" } } } },
    "/agent-card": { get: { operationId: "agentCard", responses: { "200": { description: "Agent manifest" } } } },
    "/integration/sources": { get: { operationId: "integrationSources", responses: { "200": { description: "Local source inventory" } } } },
    "/integration/scripting-map": { get: { operationId: "integrationScriptingMap", responses: { "200": { description: "Cross-application scripting map" } } } },
    "/integration/validate": { get: { operationId: "integrationValidate", responses: { "200": { description: "Integration validation" } } } },
    "/jobs": { post: { operationId: "createJob", responses: { "201": { description: "Created job" } } } },
    "/run": { post: { operationId: "runTool", requestBody: { required: true, content: { "application/json": { schema: { type: "object", required: ["tool"], properties: { tool: { type: "string" }, params: { type: "object" } } } } } }, responses: { "200": { description: "Allowlisted tool result" } } } },
    "/assets/search": { post: { operationId: "assetSearch", description: "Search semantic sources and editable SVG catalogs through the allowlisted asset.search tool.", responses: { "200": { description: "Asset search result" } } } },
    "/assets/fetch": { post: { operationId: "assetFetch", description: "Fetch a selected editable SVG through the allowlisted asset.fetch tool.", responses: { "200": { description: "Fetched SVG" } } } },
    "/assets/select": { post: { operationId: "assetSelect", description: "Download selected SVG assets and write a provenance manifest.", responses: { "200": { description: "Asset manifest" } } } },
    "/jobs/{id}": { get: { operationId: "getJob", parameters: [{ name: "id", in: "path", required: true }], responses: { "200": { description: "Job status" } } } },
    "/jobs/{id}/adobe": { get: { operationId: "adobeStatus", parameters: [{ name: "id", in: "path", required: true }], responses: { "200": { description: "Adobe result envelopes" } } } },
    "/adobe/enqueue": { post: { operationId: "adobeEnqueue", responses: { "201": { description: "Queued Adobe command" } } } },
  },
}

function authorized(request) {
  if (!token) return true
  return request.headers.authorization === `Bearer ${token}`
}

function responseHeaders(request) {
  const origin = request.headers.origin
  if (!origin || !corsOrigins.has(origin)) return { "content-type": "application/json; charset=utf-8" }
  return {
    "content-type": "application/json; charset=utf-8",
    "access-control-allow-origin": origin,
    "access-control-allow-headers": "Authorization, Content-Type",
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-max-age": "600",
    vary: "Origin",
  }
}

function send(response, status, body, request) {
  const payload = status === 204 ? "" : JSON.stringify(body, null, 2)
  response.writeHead(status, responseHeaders(request))
  response.end(payload)
}

function sendHtml(response, status, body) {
  response.writeHead(status, { "content-type": "text/html; charset=utf-8" })
  response.end(body)
}

async function body(request) {
  let value = ""
  let bytes = 0
  for await (const chunk of request) {
    bytes += Buffer.byteLength(chunk)
    if (bytes > MAX_BODY_BYTES) {
      const error = new Error(`Request body exceeds ${MAX_BODY_BYTES} bytes`)
      error.statusCode = 413
      throw error
    }
    value += chunk
  }
  return value ? JSON.parse(value) : {}
}

const server = http.createServer(async (request, response) => {
  try {
    if (request.method === "OPTIONS") return send(response, 204, {}, request)
    if (!authorized(request)) return send(response, 401, { error: "Unauthorized" }, request)
    const url = new URL(request.url, `http://${host}:${port}`)
    if (request.method === "GET" && url.pathname === "/health") return send(response, 200, { ok: true, host, port }, request)
    if (request.method === "GET" && url.pathname === "/capabilities") return send(response, 200, registry, request)
    if (request.method === "GET" && url.pathname === "/agent-card") return send(response, 200, agentCard, request)
    if (request.method === "GET" && url.pathname === "/integration/sources") return send(response, 200, await integrationSources(), request)
    if (request.method === "GET" && url.pathname === "/integration/scripting-map") return send(response, 200, await integrationScriptingMap(), request)
    if (request.method === "GET" && url.pathname === "/integration/validate") return send(response, 200, await validateIntegration(), request)
    if (request.method === "GET" && url.pathname === "/openapi.json") return send(response, 200, openApi, request)
    if (request.method === "GET" && url.pathname === "/planner") {
      const document = url.searchParams.get("document") || ""
      if (!document) return sendHtml(response, 200, renderPlanner())
      const extracted = await extractDocument(document)
      return sendHtml(response, 200, renderPlanner({ document, title: path.basename(extracted.source, path.extname(extracted.source)), pages: extracted.pages }))
    }
    if (request.method === "POST" && url.pathname === "/adobe/enqueue") {
      const payload = await body(request)
      return send(response, 201, await enqueueAdobe(payload), request)
    }
    if (request.method === "POST" && url.pathname === "/jobs") {
      const payload = await body(request)
      return send(response, 201, await createJob(payload.name || "agent-job", payload.request || {}), request)
    }
    if (request.method === "POST" && ["/assets/search", "/assets/fetch", "/assets/select"].includes(url.pathname)) {
      const payload = await body(request)
      const tool = { "/assets/search": "asset.search", "/assets/fetch": "asset.fetch", "/assets/select": "asset.select" }[url.pathname]
      if (payload.selectionPath) assertAllowedInput(payload.selectionPath, [...(config.allowedInputRoots || []), "C:\\IA\\flujo", "C:\\Users\\issvk\\claude_sesiones_recuperadas"])
      return send(response, 200, await runTool(tool, payload), request)
    }
    if (request.method === "POST" && url.pathname === "/run") {
      const payload = await body(request)
      if (!WEB_RUN_TOOLS.has(payload.tool)) return send(response, 400, { error: `Tool is not enabled for web execution: ${payload.tool}` }, request)
      if (payload.params?.image) assertAllowedInput(payload.params.image, config.allowedInputRoots)
      if (payload.params?.document) assertAllowedInput(payload.params.document, [...(config.allowedInputRoots || []), "C:\\IA\\flujo", "C:\\Users\\issvk\\claude_sesiones_recuperadas"])
      if (payload.params?.designPath) assertAllowedInput(payload.params.designPath, [...(config.allowedInputRoots || []), "C:\\IA\\flujo", "C:\\Users\\issvk\\claude_sesiones_recuperadas"])
      if (payload.params?.selectionPath) assertAllowedInput(payload.params.selectionPath, [...(config.allowedInputRoots || []), "C:\\IA\\flujo", "C:\\Users\\issvk\\claude_sesiones_recuperadas"])
      if (payload.tool?.startsWith("gdkb.") && payload.params?.input) assertAllowedInput(payload.params.input, config.allowedInputRoots)
      return send(response, 200, await runTool(payload.tool, payload.params || {}), request)
    }
    const match = url.pathname.match(/^\/jobs\/([^/]+)$/)
    const adobeMatch = url.pathname.match(/^\/jobs\/([^/]+)\/adobe$/)
    if (request.method === "GET" && adobeMatch) return send(response, 200, await adobeStatus(adobeMatch[1]), request)
    if (request.method === "GET" && match) {
      let job = await getJob(match[1])
      if (job.state === "waiting-for-adobe") {
        await adobeStatus(match[1])
        job = await getJob(match[1])
      }
      return send(response, 200, job, request)
    }
    send(response, 404, { error: "Not found" }, request)
  } catch (error) {
    send(response, error.statusCode || 500, { error: error.message }, request)
  }
})

server.listen(port, host, () => console.log(`Agent Toolkit listening on http://${host}:${port}`))
