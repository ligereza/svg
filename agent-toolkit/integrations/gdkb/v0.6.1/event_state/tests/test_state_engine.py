from app.events import Event
from app.state import build_state, StateError

def ev(i,t,e=None,target=None,p=None):
    return Event(i,t,e,target,p or {},i)

def test_rebuild_is_deterministic():
    events=[
      ev("1","ENTITY_CREATED","E1",p={"kind":"substance","canonical_name":"Alpha"}),
      ev("2","ENTITY_CREATED","E2",p={"kind":"substance","canonical_name":"Beta"}),
      ev("3","MERGE","E2","E1",{"reason":"identity evidence","evidence_ids":["EV1"]})
    ]
    a=build_state(events)
    b=build_state(events)
    assert a==b

def test_merge_preserves_history():
    events=[
      ev("1","ENTITY_CREATED","E1",p={"kind":"substance","canonical_name":"Alpha"}),
      ev("2","ENTITY_CREATED","E2",p={"kind":"substance","canonical_name":"Alpha alias"}),
      ev("3","MERGE","E2","E1",{"reason":"same identity","evidence_ids":["EV1"]})
    ]
    s=build_state(events)
    assert "E2" in s["entities"]
    assert s["entities"]["E2"]["status"]=="merged"
    assert s["merges"]["E2"]=="E1"

def test_invalid_merge_fails():
    events=[
      ev("1","ENTITY_CREATED","E1",p={"kind":"substance","canonical_name":"A"}),
      ev("2","MERGE","E1","E9",{"reason":"x","evidence_ids":["E"]})
    ]
    try:
        build_state(events)
        assert False
    except StateError:
        assert True

def test_duplicate_event_fails():
    events=[
      ev("1","ENTITY_CREATED","E1",p={"kind":"substance","canonical_name":"A"}),
      ev("1","ENTITY_CREATED","E2",p={"kind":"substance","canonical_name":"B"})
    ]
    try:
        build_state(events)
        assert False
    except StateError:
        assert True
