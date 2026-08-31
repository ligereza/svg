# Agent Toolkit

Local orchestration layer for the installed SVG, data, Blender and Adobe tools.

## Quick start

From PowerShell:

```powershell
cd C:\IA\svg\agent-toolkit
npm run tool -- list
npm run tool -- workflow image-to-svg-preview --image C:\path\to\image.png --animation float
npm run tool -- workflow image-to-svg-preview --image C:\path\to\image.png --vectorize --blender --adobe after-effects
npm run tool -- workflow image-to-svg-blender-illustrator --image C:\path\to\image.png --animation float
npm test
npm run verify
```

The workflow stages the source file in `jobs/<job-id>/input/`, then writes
working artifacts to `work/` and final artifacts to `output/`. It never writes
outside the toolkit workspace unless a future adapter explicitly requests an
approved export path.

Job lifecycle events are appended to `logs/audit.ndjson`; credentials and
request bodies are not recorded.

The combined Blender + Illustrator recipe vectorizes the source, creates the
animated SVG and browser preview, imports it into Blender for a `.blend` and
PNG render, and queues the vector SVG for Illustrator. Illustrator consumes
that command through `adapters/adobe/illustrator/agent.jsx`.

The toolkit also integrates GDKB 0.6.1 as a knowledge layer for semantic asset
search. Its original slices are preserved under
`integrations/gdkb/v0.6.1/`; the local Python bridge is exposed through the
`gdkb.*` tools and is used by `asset.search` for normalization and conservative
identity review.

## Commands

```text
list                                      List registered capabilities
job create --name NAME                    Create a job envelope
svg create --spec FILE --output FILE      Create SVG from JSON
svg embed-image --image FILE --output FILE
svg rasterize --input FILE --output jobs/manual/output/fallback.png --width 2048
svg vectorize --image FILE --output FILE
svg animate --input FILE --output FILE --animation float
svg particles --output FILE --count 40
svg validate --input FILE
svg preview --input FILE --output FILE
svg thi-ng-geom --spec geometry.json --output jobs/manual/output/thi-ng.svg
data chart --input FILE --output FILE --x LABEL --y VALUE
data d3-chart --input FILE --output jobs/manual/output/d3-chart.svg --x LABEL --y VALUE
data animate --input FILE --output FILE --duration-ms 1200
image split --input FILE --output jobs/manual/output/tiles.json --rows 2 --columns 2
image extract-checkerboard-matte --input FILE --output jobs/manual/output/iconos.json --rows 1 --columns 1 --orphan-area 64 --grabcut-iterations 5
image extract-checkerboard-matte --plan plan.json --output output/manifest.json --assets-dir output --padding 18
blender run --operation create-scene --spec FILE --output FILE
blender run --operation layout-scene --spec storyboard-with-assets.json --output jobs/manual/output/slides.blend --render-output jobs/manual/output/slides.png
blender run --operation export-glb --spec FILE --output jobs/manual/output/scene.glb
blender run --operation import-glb --spec FILE.glb --output jobs/manual/output/scene.blend --render-output jobs/manual/output/scene.png
scene3d create --spec scene.example.json --output jobs/manual/output/scene.html
math stdlib-stats --values "[1,2,3,4]" --output jobs/manual/output/stats.json
workflow rxjs-events --events "[{\"type\":\"render\"},{\"type\":\"export\"}]"
workflow effect-retry --failures-before-success 2 --max-retries 3 --value render
adobe enqueue --app photoshop --operation import-svg --input FILE
photoshop separate-objects --input FILE --mode subject --output separated/manifest.json --psd-output separated/objects.psd
photoshop separate-objects --input FILE --mode regions --objects regions.json --output separated/manifest.json --psd-output separated/objects.psd
adobe status --job JOB_ID
adobe render --project PROJECT.aep --output jobs/manual/output/render
workflow image-to-svg-preview --image FILE
workflow image-to-svg-blender-illustrator --image FILE
workflow document-to-animated-post --document FILE.pdf --title "TITLE" --max-parts 8 --pdf-provider local
For Adobe PDF Services, set `PDF_SERVICES_CLIENT_ID` and `PDF_SERVICES_CLIENT_SECRET`, or set `PDF_SERVICES_CREDENTIALS` to the downloaded credential JSON, then run the same workflow with `--pdf-provider adobe`. `--pdf-provider auto` uses Adobe only when credentials are configured; otherwise it keeps the local extractor.
workflow multi-app-composition --storyboard storyboard.json --project-root projects/chemsex --adobe photoshop --adobe-operation separate-objects
asset search --query "MDMA" --terms chemsex --providers all --ancla "texto exacto" --role "illustration" --output jobs/manual/output/asset-search.json
asset fetch --provider iconify --id material-symbols:pill --output jobs/manual/output/pill.svg
asset select --selection jobs/manual/output/asset-search.json --selected iconify:material-symbols:pill --ancla "texto exacto" --role "illustration" --output jobs/manual/output/asset-manifest.json
gdkb health
gdkb normalize --value "Cocaína"
gdkb import --input integrations/gdkb/v0.6.1/import_engine/fixtures/pubchem_small.jsonl
gdkb replay --input integrations/gdkb/v0.6.1/event_state/fixtures/event_sequence.json --snapshot-id S1
integration sources
integration scripting-map
integration validate
integration plan --source projects/chemsex/storyboard.json

All file-producing commands reject existing outputs by default. Add `--force`
when replacing an existing artifact is intentional.

## Asset search workflow

`asset.search` separates the research layer from the visual layer:

1. PubChem resolves compound names and properties.
2. ChEBI resolves chemical identity and ontology.
3. OLS searches broader biomedical concepts.
4. The resulting terms generate visual suggestions.
5. Iconify searches general editable SVG icons.
6. Bioicons searches biology and chemistry SVGs from its open catalog.

## MobileCLIP local semantic search

Context Shelf can optionally rank the local catalog with the original MobileCLIP v1 checkpoint from Apple. The semantic layer is additive: lexical search continues to work when the Python runtime, checkpoint or vector index is unavailable.

The checkpoint is downloaded only from the official Apple host and its expected size and SHA-256 digest are checked before it can be loaded. The worker uses `torch.load(weights_only=True)` and refuses runtimes that would require unsafe checkpoint unpickling. MobileCLIP S2 is the default because it is a good quality/latency balance for thousands of icons.

The one-time setup is explicit:

```powershell
git clone https://github.com/apple/ml-mobileclip.git cache/context-shelf/mobileclip/ml-mobileclip
python -m pip install torch torchvision pillow cairosvg
npm run tool -- semantic install --model mobileclip_s2
npm run tool -- semantic status --model mobileclip_s2
npm run tool -- semantic index --model mobileclip_s2 --batch-size 48
```

For the GPU-optimized fixed-batch graph, run the one-time export from the
existing export environment (it is CPU-only and does not download a model):

```powershell
cache\context-shelf\mobileclip\export-venv\Scripts\python.exe scripts\mobileclip-export.py --model-name mobileclip_s2 --checkpoint cache\context-shelf\mobileclip\mobileclip_s2.pt --repo-path cache\context-shelf\mobileclip\ml-mobileclip --output-dir cache\context-shelf\mobileclip --opset 17 --image-batch-size 96
npm run tool -- semantic index --model mobileclip_s2 --batch-size 96
```

When `mobileclip_s2.image.b96.onnx` exists and the index batch size is 96,
the indexer selects it automatically. The last partial batch is padded only
for the model call and its extra embeddings are discarded. The dynamic graph
remains the fallback for other batch sizes or installations without the
fixed graph.

After the index is generated, the companion search automatically requests the semantic ranker. The direct CLI equivalent is:

```powershell
npm run tool -- asset search-local --query "pulmones" --semantic
```

Set `MOBILECLIP_PYTHON` when the model environment uses a different Python executable, and `MOBILECLIP_REPO` when the official Apple repository is stored elsewhere. The original MobileCLIP v1 checkpoint is used here; MobileCLIP2 is intentionally excluded because its official distribution currently points to Hugging Face.
7. `asset.select` downloads the chosen SVGs and writes a provenance manifest
with the exact text/ancla, source URL, asset id and license.

## Blender asset contract

`blender.layout-scene` accepts `assets` inline or an `assetManifest` path. Each
asset can declare `slideId`, `slideIndex`/`slideNumber`, or use a filename such
as `slide-03-icon.svg` for deterministic assignment. The importer accepts SVG,
PNG, JPG, WebP, TIFF and EXR. SVGs remain editable 2D curves by default and
support `convertToMesh: true` when a downstream Geometry Nodes operation needs
mesh input. Use `importMode: "curves"|"mesh"|"raster"`; the raster mode uses
CairoSVG for exact visual fallback when the source contains filters, text or
complex gradients. Use `anchor: "illustration"|"text"|"full"`, `fit: "contain"|"cover"|"stretch"`,
`zIndex`, `defaultColor` and `pack` for placement and reproducibility.

SVG colors are converted to emission materials, CSS classes and opacity are
preserved where supported, and layer order receives deterministic Z offsets.
Raster assets use sRGB textures and emission, so Cycles lighting does not
unintentionally darken Firefly or other generated images.

Each imported primitive receives the reusable `GN_Asset_2D_Transform` modifier
with `Scale X`, `Scale Y`, `Offset X`, `Offset Y`, `Rotation` and `Pulse` inputs.
Those controls are keyframeable in Blender and stay attached to the asset root.
For a production render, add for example
`"render": {"mode": "slide", "slide": 2, "showGuides": false }` to the
storyboard. Blender then renders that slide at the declared canvas size
(for example `1080×1440` for the Chemsex portrait project) while keeping the editable scene intact. Omit
`render` or use `"mode": "sheet"` for the review board with layout guides.

## Multi-application integration

The source inventory is machine-readable in
[`integrations/tool-sources.json`](integrations/tool-sources.json). It tracks
thi.ng umbrella, D3, three.js, Effect, RxJS, stdlib, GDKB, Blender and Adobe.
`available-source` means the code is present and ready for a declared wrapper;
`integrated-runtime` means the toolkit invokes an adapter today.

The contracts and script surfaces are in
[`integrations/scripting-map.json`](integrations/scripting-map.json). The full
recipe, including Photoshop/Illustrator boundaries and Geometry Nodes controls,
is in [`INTEGRATION-GUIDE.md`](INTEGRATION-GUIDE.md).

For Chemsex, [`projects/chemsex/PROJECT.json`](projects/chemsex/PROJECT.json)
is the project-level source of truth: 1080×1440 px, exact source order, PSD and
Blender artifact roots. Jobs remain auditable under `jobs/`; project deliverables
are copied into the project root when `--project-root` is supplied.

The canonical Chemsex regenerated-layer workflow and its mechanical Python
entry point are documented in
[`projects/chemsex/editable/blender/chemsex-carousel-all-slides/README.md`](projects/chemsex/editable/blender/chemsex-carousel-all-slides/README.md).
Do not create a parallel PNG-to-SVG workflow for that project: the PNG is a
visual reference only, layers are regenerated semantically, masks are mandatory,
and the deterministic packaging is centralized in
`experiments/layer-decompose/chemsex_layer_pipeline.py`.

Use these checks before starting a new project:

```powershell
npm run tool -- integration sources
npm run tool -- integration validate
npm run tool -- integration plan --source projects/chemsex/storyboard.json
```

## Photoshop object separation

When a generated raster image needs to become editable, use Photoshop as the
segmentation stage instead of importing the whole image as one plane. The
`photoshop.separate-objects` command queues a Photoshop UXP/JSX operation that
keeps an editable PSD layer per object, exports transparent cropped PNGs and
writes a manifest with normalized canvas placement. When Photoshop's automatic
selection is used, the PSD receives a transparent object layer; rectangle mode
keeps a non-destructive layer mask. Feed that manifest to
`blender.layout-scene` through `assetManifest`; each object then receives its
own Geometry Nodes transform controls. A Photoshop manifest is marked
`singleSlide`, so it maps automatically to the first part of a one-slide
storyboard; for a multi-slide carousel, add the desired `slideNumber` to each
asset or generate one manifest per slide.

Use `--mode subject` for Photoshop's automatic main-subject cutout. Use
`--mode regions --objects regions.json` when the composition contains several
objects and you want editable divisions. Region entries use
`"selectionMode": "object"` by default: Photoshop first tries Select Subject
inside that region and falls back to a rectangle mask if the detector returns
an empty or unusable selection. Set `"selectionMode": "rectangle"` when the
designer intentionally wants the region itself. The manifest records
`selectionMethod` and any `selectionError`, so a failed AI cutout is visible
instead of silently being treated as a successful object extraction.

The search is cached for 24 hours in `cache/asset-search/`. The cache is local,
ignored by Git and can be removed without affecting the source project. Search
results are suggestions: the designer still chooses the visual asset and the
document text is never rewritten by this tool.

## GDKB knowledge layer

The integrated GDKB project supplies identity, evidence, provenance, imports,
event replay, snapshots and lifecycle decisions. It is intentionally exposed
as a separate layer from the SVG generator: scientific identity can inform a
visual search, but it does not silently rewrite the source document or merge
entities without evidence. See
[`integrations/gdkb/v0.6.1/README.md`](integrations/gdkb/v0.6.1/README.md).

## Runtime boundaries

The Node orchestrator owns job state and pure file transformations. Blender is
called through `adapters/blender/agent_blender.py`. Adobe hosts consume command
envelopes from `jobs/<id>/adobe/commands/` through their own script/plugin.

See [CAPABILITIES.md](CAPABILITIES.md) for the agent-facing map.
See [PROJECT-STATUS.md](PROJECT-STATUS.md) for the requirement-by-requirement
verification audit and the remaining external dependencies.
See [INTEGRATION-GUIDE.md](INTEGRATION-GUIDE.md) for the scripting and host
integration contract.
