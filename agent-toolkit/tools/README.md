# Tools entrypoint

The executable tool implementations live in `src/tools/` so Node can import
them as a single runtime module. This top-level directory is the agent-facing
catalog entrypoint for the toolkit layout:

| Capability family | Runtime implementation |
|---|---|
| SVG creation, embedding, animation, particles, validation and preview | `src/tools/svg.mjs` |
| Raster-to-path conversion | `src/tools/vectorize.mjs` + `adapters/image/vectorize.py` |
| Data charts and chart animation | `src/tools/chart.mjs` |

Use `registry.json` as the authoritative list of callable tools and their
input/output contracts.
