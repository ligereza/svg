CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;

CREATE TABLE IF NOT EXISTS source (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL UNIQUE,
  publisher TEXT,
  source_type TEXT NOT NULL,
  url TEXT,
  version TEXT,
  license TEXT
);

CREATE TABLE IF NOT EXISTS entity (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  kind TEXT NOT NULL,
  canonical_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS entity_name_trgm
  ON entity USING GIN (canonical_name gin_trgm_ops);

CREATE TABLE IF NOT EXISTS source_record (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_id UUID NOT NULL REFERENCES source(id),
  external_id TEXT NOT NULL,
  record_type TEXT,
  payload JSONB NOT NULL,
  payload_hash TEXT NOT NULL,
  retrieved_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(source_id, external_id)
);

CREATE TABLE IF NOT EXISTS entity_name (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entity_id UUID NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
  value TEXT NOT NULL,
  normalized_value TEXT NOT NULL,
  language_code TEXT,
  country_code CHAR(2),
  name_type TEXT NOT NULL DEFAULT 'unknown',
  preferred BOOLEAN NOT NULL DEFAULT false,
  source_record_id UUID REFERENCES source_record(id),
  UNIQUE(entity_id, value, language_code, country_code)
);
CREATE INDEX IF NOT EXISTS entity_name_normalized_trgm
  ON entity_name USING GIN (normalized_value gin_trgm_ops);

CREATE TABLE IF NOT EXISTS external_identifier (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  entity_id UUID NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
  source_id UUID NOT NULL REFERENCES source(id),
  identifier_type TEXT NOT NULL,
  identifier_value TEXT NOT NULL,
  source_record_id UUID REFERENCES source_record(id),
  UNIQUE(source_id, identifier_type, identifier_value)
);

CREATE TABLE IF NOT EXISTS assertion (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  subject_id UUID NOT NULL REFERENCES entity(id) ON DELETE CASCADE,
  predicate TEXT NOT NULL,
  object_entity_id UUID REFERENCES entity(id) ON DELETE CASCADE,
  object_value JSONB,
  source_record_id UUID REFERENCES source_record(id),
  confidence NUMERIC(6,5),
  status TEXT NOT NULL DEFAULT 'asserted',
  valid_from DATE,
  valid_until DATE,
  CHECK (object_entity_id IS NOT NULL OR object_value IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS review_task (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  input_value TEXT NOT NULL,
  normalized_value TEXT NOT NULL,
  candidate_entity_id UUID REFERENCES entity(id),
  score NUMERIC(6,5),
  reason TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  decision TEXT,
  reviewer TEXT,
  reviewed_at TIMESTAMPTZ,
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
