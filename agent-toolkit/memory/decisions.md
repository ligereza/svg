# Architecture decisions

## 2026-08-16 — File-based job boundary

The orchestrator communicates with desktop hosts through a job directory and
JSON envelopes. This keeps the web agent independent from Blender's Python
runtime and Adobe's host-specific scripting runtime.

## 2026-08-16 — Localhost-only server by default

The HTTP server binds to `127.0.0.1`. A bearer token can be enabled with
`AGENT_TOOLKIT_TOKEN` before exposing it through a deliberate bridge or tunnel.
No arbitrary shell endpoint is exposed.

## 2026-08-16 — Blender version

Blender 5.1 is the configured default because it is installed and the create
scene/render smoke tests passed. The adapter can be pointed at another version
through `config.local.json`.

## 2026-08-17 — Adobe host boundary

Legacy Adobe ExtendScript hosts do not reliably provide the modern `JSON`
global, so JSX consumers include `adapters/adobe/json-compat.jsxinc`. The
Illustrator consumer was validated through its Windows COM automation path:
it imported a real queued SVG and wrote a completed result envelope. Photoshop
The Photoshop JSX/COM fallback is now verified for SVG import/export; direct
Photoshop UXP, After Effects, and Premiere remain host-pending.
