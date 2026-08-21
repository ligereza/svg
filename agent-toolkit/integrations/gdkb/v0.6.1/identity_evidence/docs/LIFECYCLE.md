# Entity Lifecycle

Entity lifecycle events are append-only.

## Merge

When A and B are determined to represent the same entity:

```text
A ──merged_into──> B
```

A is not deleted.

Its names, identifiers, observations and assertions remain historically
traceable.

## Split

If an entity was incorrectly merged:

```text
A
├──split_into──> B
└──split_into──> C
```

The split records the reason, evidence and timestamp.

## Supersede

Used when a representation is replaced without claiming strict identity:

```text
A ──superseded_by──> B
```

## Redirect

Used when an identifier should resolve to another entity.

## Deprecate / restore

An entity can be made inactive without deleting its history.

## Rule

No destructive merge/delete operation is allowed in the canonical history.
