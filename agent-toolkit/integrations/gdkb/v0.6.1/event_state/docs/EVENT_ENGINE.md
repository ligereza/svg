# Event & State Engine — 0.6.1

The canonical history is an ordered event stream.

## Event sourcing rule

The materialized state is derived:

```text
events  →  state
```

The event log is the historical authority.

## Determinism

Given the same:

- event sequence
- state-builder version

the same state hash must be produced.

## Merge

Merge changes lifecycle state but does not delete the source entity.

## Snapshot

A snapshot stores:

- event boundary
- reconstructed state
- state hash

This allows fast reads while preserving event history.

## Current limitations

The prototype state builder is intentionally small.

Before production:

- event schemas need versioning
- transactional database constraints need testing
- split semantics need a formal state transition model
- snapshot compaction needs specification
- event replay needs migration tests
