import test from "node:test"
import assert from "node:assert/strict"
import { normalizeStructuredData, parseEnvText, pdfServicesConfigured } from "../src/adapters/pdf-services.mjs"

test("PDF Services env parser keeps only supported variables and removes quotes", () => {
  assert.deepEqual(parseEnvText([
    "PDF_SERVICES_CLIENT_ID=client-id",
    'PDF_SERVICES_CLIENT_SECRET="client-secret"',
    "OTHER_SECRET=must-not-load",
    "export PDF_SERVICES_CREDENTIALS='credentials.json'",
  ].join("\n")), {
    PDF_SERVICES_CLIENT_ID: "client-id",
    PDF_SERVICES_CLIENT_SECRET: "client-secret",
    PDF_SERVICES_CREDENTIALS: "credentials.json",
  })
})

test("PDF Services normalizer preserves reading order, pages and layout bounds", () => {
  const result = normalizeStructuredData({
    pages: [{ pageNumber: 0, width: 720, height: 720 }, { pageNumber: 1, width: 720, height: 720 }],
    elements: [
      { Path: "//Document/H1", Text: "Portada", Page: 1, Bounds: [10, 20, 300, 80], TextSize: 32 },
      { Path: "//Document/P", Text: "Texto exacto", Page: 1, Bounds: [10, 90, 300, 130] },
      { Path: "//Document/Figure", Page: 2, Bounds: [50, 50, 500, 600], FilePaths: ["figures/figure-1.png"] },
    ],
  }, { source: "input.pdf", artifacts: ["figures/figure-1.png"] })
  assert.equal(result.provider, "adobe-pdf-services")
  assert.equal(result.pages, 2)
  assert.match(result.text, /\[\[PAGE 1\]\][\s\S]*Portada[\s\S]*Texto exacto[\s\S]*\[\[PAGE 2\]\]/)
  assert.equal(result.layout[0].type, "h1")
  assert.deepEqual(result.layout[0].bounds, [10, 20, 300, 80])
  assert.deepEqual(result.assets, ["figures/figure-1.png"])
})

test("PDF Services reports not configured without exposing secrets", async () => {
  const previous = {
    id: process.env.PDF_SERVICES_CLIENT_ID,
    secret: process.env.PDF_SERVICES_CLIENT_SECRET,
    file: process.env.PDF_SERVICES_CREDENTIALS,
  }
  delete process.env.PDF_SERVICES_CLIENT_ID
  delete process.env.PDF_SERVICES_CLIENT_SECRET
  delete process.env.PDF_SERVICES_CREDENTIALS
  assert.equal(await pdfServicesConfigured({ loadDotEnv: false }), false)
  if (previous.id === undefined) delete process.env.PDF_SERVICES_CLIENT_ID
  else process.env.PDF_SERVICES_CLIENT_ID = previous.id
  if (previous.secret === undefined) delete process.env.PDF_SERVICES_CLIENT_SECRET
  else process.env.PDF_SERVICES_CLIENT_SECRET = previous.secret
  if (previous.file === undefined) delete process.env.PDF_SERVICES_CREDENTIALS
  else process.env.PDF_SERVICES_CREDENTIALS = previous.file
})
