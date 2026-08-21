# Identity Model

## Entity identity

```text
entity_id
entity_kind
status
created_at
```

`entity_id` is generated internally and must not be derived directly from
a source identifier.

## Entity kinds

The initial controlled vocabulary:

- substance
- chemical_class
- product
- preparation
- mixture
- biological_entity
- effect
- risk
- legal_concept
- other

This avoids forcing every object into "drug" or "chemical".

## Chemical identity

Chemical identity may include:

- InChI
- InChIKey
- canonical structure representation
- molecular formula
- molecular weight
- CAS and other registry identifiers

These are evidence-bearing identifiers, not automatically interchangeable
definitions of identity.

## Names

Names have attributes:

```text
value
normalized_value
language
country
region
name_type
valid_from
valid_until
source
```

`name_type` examples:

- preferred
- synonym
- translation
- historical
- regional
- abbreviation
- brand
- colloquial
- misspelling

Original spelling is always retained.

## Important distinction

A translation is not automatically a synonym.
A brand is not automatically a chemical substance.
A salt is not automatically the same entity as its parent.
