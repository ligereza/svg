CREATE TABLE IF NOT EXISTS event_log (
  sequence BIGSERIAL PRIMARY KEY,
  event_id UUID NOT NULL UNIQUE,
  event_type TEXT NOT NULL,
  entity_id UUID,
  target_entity_id UUID,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS event_log_entity
ON event_log(entity_id, sequence);

CREATE TABLE IF NOT EXISTS snapshot_state (
  snapshot_id UUID PRIMARY KEY,
  event_end BIGINT NOT NULL,
  state_hash TEXT NOT NULL,
  state JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS snapshot_event_end
ON snapshot_state(event_end);
