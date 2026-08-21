# 0.6.1 Core Implementation Notes

This slice deliberately makes the resolver conservative.

### Why?

An incorrect merge is contagious:
one mistaken identity can attach aliases, identifiers, classifications and downstream claims to the wrong entity.

Therefore:

- identifier evidence can confirm only when unique
- exact names still require contextual confidence
- fuzzy matching only produces candidates
- ambiguous matches enter review
- source records are immutable inputs
- normalized values are derived fields
- original source values remain available

The next engineering task is not adding more drug data. It is wiring the source adapters into this model with idempotent imports and fixture-based tests.
