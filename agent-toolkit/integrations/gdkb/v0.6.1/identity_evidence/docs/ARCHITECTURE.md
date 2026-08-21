# Architecture — 0.6.1

## Layer 1: Identity

An internal entity represents a stable conceptual identity.

For chemical substances, structural identifiers may contribute evidence,
but no single external database is treated as the owner of identity.

```text
ENTITY
 ├── names
 ├── external identifiers
 ├── structural representations
 └── lifecycle
```

## Layer 2: Observation

An observation records what a source supplied at a point in time.

```text
SOURCE
  ↓
OBSERVATION
```

An observation preserves the original value and source metadata.

## Layer 3: Assertion

An assertion is a normalized semantic statement derived from one or more
observations.

```text
OBSERVATION
   ↓
ASSERTION
```

An assertion retains provenance. It does not become an unqualified fact.

## Layer 4: Decision

A resolver makes a decision about an input:

```text
confirmed
candidate
needs_review
rejected
```

A decision is distinct from the evidence used to reach it.

## Layer 5: Lifecycle

Entities can change representation without erasing history:

```text
merge
split
supersede
redirect
deprecate
restore
```

All lifecycle events are append-only.
