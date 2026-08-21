# Evidence Model

## Source

Describes the publisher or dataset.

## Observation

A source-specific observation:

```text
source
external_record_id
observed_at
retrieved_at
raw_value
payload_hash
source_version
```

## Evidence

Evidence is a typed interpretation of an observation:

```text
evidence_type
observation_id
target_entity
strength
method
```

Examples:

- exact_identifier
- exact_structure
- source_mapping
- exact_name
- translated_name
- fuzzy_name
- human_review

## Assertion

```text
subject
predicate
object
evidence[]
status
validity
```

The same assertion can have multiple supporting observations.

Contradictory assertions are retained rather than overwritten.

## Confidence

Do not collapse everything into one arbitrary number.

Track separately:

```text
source_authority
evidence_strength
identity_confidence
decision_confidence
```

A derived score may be calculated later, but raw components remain available.
