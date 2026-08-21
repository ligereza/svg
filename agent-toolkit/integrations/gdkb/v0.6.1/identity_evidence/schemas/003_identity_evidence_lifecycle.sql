CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS entity (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  kind TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  canonical_name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS source (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL UNIQUE,
  publisher TEXT,
  source_type TEXT NOT NULL,
  version TEXT,
  license TEXT,
  url TEXT
);

CREATE TABLE IF NOT EXISTS observation (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_id UUID NOT NULL REFERENCES source(id),
  external_record_id TEXT NOT NULL,
  observed_at TIMESTAMPTZ,
  retrieved_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  source_version TEXT,
  raw_value JSONB NOT NULL,
  payload_hash TEXT NOT NULL,
  UNIQUE(source_id, external_record_id, payload_hash)
);

CREATE TABLE IF NOT EXISTS identifier_observation (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  observation_id UUID NOT NULL REFERENCES observation(id) ON DELETE CASCADE,
  identifier_type TEXT NOT NULL,
  identifier_value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS name_observation (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  observation_id UUID NOT NULL REFERENCES observation(id) ON DELETE CASCADE,
  value TEXT NOT NULL,
  normalized_value TEXT NOT NULL,
  language_code TEXT,
  country_code CHAR(2),
  region TEXT,
  name_type TEXT
);

CREATE TABLE IF NOT EXISTS evidence (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  observation_id UUID REFERENCES observation(id),
  evidence_type TEXT NOT NULL,
  target_entity_id UUID REFERENCES entity(id),
  strength NUMERIC(6,5),
  method TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS assertion (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  subject_entity_id UUID NOT NULL REFERENCES entity(id),
  predicate TEXT NOT NULL,
  object_entity_id UUID REFERENCES entity(id),
  object_value JSONB,
  status TEXT NOT NULL DEFAULT 'asserted',
  valid_from DATE,
  valid_until DATE
);

CREATE TABLE IF NOT EXISTS assertion_evidence (
  assertion_id UUID NOT NULL REFERENCES assertion(id) ON DELETE CASCADE,
  evidence_id UUID NOT NULL REFERENCES evidence(id) ON DELETE CASCADE,
  PRIMARY KEY(assertion_id, evidence_id)
);

CREATE TABLE IF NOT EXISTS resolution_decision (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  input_value TEXT NOT NULL,
  normalized_value TEXT NOT NULL,
  candidate_entity_id UUID REFERENCES entity(id),
  decision TEXT NOT NULL,
  decision_confidence NUMERIC(6,5),
  reason TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS entity_event (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  event_type TEXT NOT NULL,
  entity_id UUID REFERENCES entity(id),
  target_entity_id UUID REFERENCES entity(id),
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS snapshot (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  label TEXT NOT NULL,
  schema_version TEXT NOT NULL,
  importer_version TEXT,
  resolver_version TEXT,
  manifest_hash TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
