# GDKB 0.6.1 — Core

This is the next implementation slice after the architectural restructuring.

Run tests:

```bash
python -m pytest
```

The core currently covers:

- deterministic normalization
- conservative entity resolution
- immutable source-record concept
- canonical entities
- multilingual names
- external identifiers
- provenance-ready assertions
- review queue
- snapshot metadata
- a small gold benchmark

The resolver intentionally refuses to auto-merge on fuzzy similarity alone.
