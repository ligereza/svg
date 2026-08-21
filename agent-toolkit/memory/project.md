# Project memory

## Current scope

Build a local, low-context agent toolkit that coordinates SVG tools, Blender
and Adobe applications through isolated jobs and explicit adapters.

## Installed source repositories

- `C:\IA\svg\umbrella`
- `C:\IA\svg\d3`
- `C:\IA\svg\three.js`
- `C:\IA\svg\effect`
- `C:\IA\svg\rxjs`
- `C:\IA\svg\stdlib`

## First verified workflow

`image -> embedded SVG -> animation -> HTML preview`

## Extended verified workflows

- `image -> vectorized SVG -> animation -> HTML preview -> Blender render`
  (Blender 5.1)
- `image -> vectorized SVG -> animation -> HTML preview -> Illustrator import`
  (Illustrator 2026 JSX/COM fallback)
- `image -> vectorized SVG -> animation -> HTML preview -> Photoshop import/export`
  (Photoshop 2026 JSX/COM fallback)

## Important constraints

- Tools must be allowlisted; no arbitrary shell endpoint.
- Jobs must stay inside `agent-toolkit/jobs`.
- Adobe commands are queued through files until a host-specific plugin consumes them.
- Blender runs in background mode with a dedicated Python adapter.
