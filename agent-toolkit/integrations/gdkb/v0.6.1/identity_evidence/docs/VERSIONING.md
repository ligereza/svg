# Versioning and Snapshots

Two concepts are kept separate.

## Event history

Records what happened:

```text
observation added
observation changed
entity merged
entity split
assertion added
assertion retired
```

## Snapshot

A reproducible materialized view at a point in time.

A snapshot manifest contains:

- schema version
- importer version
- resolver version
- source versions
- retrieval cutoffs
- event range
- manifest hash

## Diff

Snapshots can report:

```text
added
removed
changed
merged
split
unchanged
```

A snapshot is never the authoritative history; the event/evidence history is.
