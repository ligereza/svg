from app.snapshot import state_hash, snapshot, diff

def test_hash_is_stable():
    s={"entities":{"E":{"id":"E"}},"events_applied":["1"]}
    assert state_hash(s)==state_hash({"events_applied":["1"],"entities":{"E":{"id":"E"}}})

def test_snapshot_contains_reconstruction_boundary():
    s={"entities":{},"events_applied":["1","2"]}
    snap=snapshot(s,"S1",2)
    assert snap["event_end"]==2
    assert len(snap["state_hash"])==64

def test_diff_detects_change():
    assert "entities" in diff({"entities":{"A":1}},{"entities":{"A":2}})
