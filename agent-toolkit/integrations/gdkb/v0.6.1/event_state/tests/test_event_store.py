from app.events import Event
from app.event_store import InMemoryEventStore

def test_append_and_replay_boundary():
    store=InMemoryEventStore()
    store.append(Event("1","ENTITY_CREATED","E1",payload={"kind":"substance","canonical_name":"A"},sequence=1))
    store.append(Event("2","ENTITY_CREATED","E2",payload={"kind":"substance","canonical_name":"B"},sequence=2))
    assert len(store.up_to(1))==1
    assert len(store.all())==2

def test_sequence_monotonic():
    store=InMemoryEventStore()
    store.append(Event("1","ENTITY_CREATED","E1",payload={},sequence=1))
    try:
        store.append(Event("2","ENTITY_CREATED","E2",payload={},sequence=1))
        assert False
    except ValueError:
        assert True
