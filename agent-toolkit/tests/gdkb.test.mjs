import test from "node:test"
import assert from "node:assert/strict"
import path from "node:path"
import { gdkbHealth, gdkbImportJsonl, gdkbMergeEvent, gdkbNormalize, gdkbReplay, gdkbResolve } from "../src/tools/gdkb.mjs"

const root = process.cwd()
const fixture = path.join(root, "integrations", "gdkb", "v0.6.1", "import_engine", "fixtures", "pubchem_small.jsonl")

test("GDKB bridge exposes the integrated runtime", async () => {
  const result = await gdkbHealth()
  assert.equal(result.name, "GDKB")
  assert.equal(result.version, "0.6.1")
  assert.ok(result.operations.includes("replay"))
})

test("GDKB preserves source values while normalizing names", async () => {
  const result = await gdkbNormalize("Cocaína")
  assert.equal(result.value, "Cocaína")
  assert.equal(result.normalized, "cocaina")
})

test("GDKB fixture import is deterministic and hashes payloads", async () => {
  const result = await gdkbImportJsonl(fixture)
  assert.equal(result.count, 3)
  assert.equal(result.records[1].payload.normalized_name, "cocaine")
  assert.equal(result.records[1].payload_hash.length, 64)
})

test("GDKB resolver keeps fuzzy matches out of confirmed state", async () => {
  const result = await gdkbResolve("cocaina", [{ id: "E1", label: "cocaine", source: "fixture" }])
  assert.equal(result.decision, "candidate")
  assert.equal(result.entity_id, "E1")
})

test("GDKB replay creates deterministic snapshots and non-destructive merges", async () => {
  const result = await gdkbReplay([
    { id: "1", event_type: "ENTITY_CREATED", entity_id: "E1", payload: { kind: "substance", canonical_name: "Alpha" }, sequence: 1 },
    { id: "2", event_type: "ENTITY_CREATED", entity_id: "E2", payload: { kind: "substance", canonical_name: "Alpha alias" }, sequence: 2 },
    { id: "3", event_type: "MERGE", entity_id: "E2", target_entity_id: "E1", payload: { evidence_ids: ["EV1"] }, sequence: 3 },
  ], { snapshot_id: "S1" })
  assert.equal(result.state.entities.E2.status, "merged")
  assert.equal(result.state.merges.E2, "E1")
  assert.equal(result.snapshot.event_end, 3)
  assert.equal(result.snapshot.state_hash.length, 64)
})

test("GDKB merge event requires evidence", async () => {
  const event = await gdkbMergeEvent({ source_entity_id: "E2", target_entity_id: "E1", reason: "same identity", evidence_ids: ["EV1"] })
  assert.equal(event.event_type, "merge")
  assert.deepEqual(event.payload.evidence_ids, ["EV1"])
})
