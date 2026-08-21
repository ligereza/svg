# 0.6.1 Import Engine

The import engine is intentionally source-agnostic.

## Pipeline

```text
fixture/API
   ↓
parse
   ↓
validate
   ↓
canonicalize payload
   ↓
hash
   ↓
persist source record
   ↓
derive normalized fields
   ↓
identity resolution
   ↓
entity/assertion updates
   ↓
snapshot
```

## Idempotency

The immutable source record is keyed by:

```text
source_name + external_id + payload_hash
```

If the same source record is imported twice, its content hash is identical.

If the external record changes, the new payload receives a different hash and can be represented as a new observation.

## Important distinction

A source record is not an entity.

For example:

```text
PubChem CID:2
PubChem CID:3
Wikidata Q1997
```

may all refer to one internal entity.

The importer stores the observations first; resolution decides identity separately.

## Next test

The next step is to connect this fixture importer to PostgreSQL and prove:

1. first import creates records
2. second identical import creates no duplicate
3. changed payload creates a new observation
4. resolution links CID:2 and CID:3 to one entity
5. ambiguous mappings enter review
