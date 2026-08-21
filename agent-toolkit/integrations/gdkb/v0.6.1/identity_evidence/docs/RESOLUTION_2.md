# Resolver 2.0

The resolver is a pipeline, not a single score.

```text
INPUT
  ↓
NORMALIZATION
  ↓
CANDIDATE GENERATION
  ↓
CANDIDATE RANKING
  ↓
EVIDENCE AGGREGATION
  ↓
DECISION
```

## Candidate generation

Sources include:

- exact internal identifier
- validated external identifier
- exact normalized name
- source-specific mapping
- structure identity
- multilingual alias
- transliteration
- fuzzy similarity

## Ranking

Candidate ranking may combine multiple independent signals.

A high string similarity is not sufficient for confirmation.

## Decisions

### confirmed

Evidence is sufficiently strong and non-conflicting.

### needs_review

Plausible candidate(s), but ambiguity or conflicting evidence remains.

### candidate

Weak evidence; retained for possible future resolution.

### rejected

Evidence indicates that the candidate is not the same entity.

## Hard safety rule

Fuzzy similarity alone can never produce `confirmed`.

## Calibration

Scores become meaningful only after evaluation against a manually verified gold set.
