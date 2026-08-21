# GDKB v0.6.1 — Identity / Evidence Restructure

This revision deliberately pauses source-scale ingestion.

The core is now organized around four independent concepts:

```text
IDENTITY
EVIDENCE
ASSERTION
LIFECYCLE
```

The database should describe what an entity is, what sources observed or asserted,
and how our internal representation changed over time.

## Critical principles

1. A name is not an identity.
2. A source record is not an entity.
3. An assertion is not universal truth.
4. A fuzzy match is not a merge.
5. A merge is reversible/auditable.
6. A snapshot is a state, not a replacement for history.
7. Source disagreement is retained.
8. Original values are never destroyed by normalization.

## Scope of this slice

- identity model
- observations/evidence
- assertions
- entity lifecycle
- merge/split/redirect events
- snapshot model
- resolver decision model
- benchmark structure

The import engine from the previous prototype is retained conceptually,
but adapters and production persistence are intentionally deferred.
