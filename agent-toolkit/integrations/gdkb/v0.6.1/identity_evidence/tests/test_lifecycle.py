from app.lifecycle import MergePlan, merge_event
import pytest

def test_merge_requires_evidence():
    with pytest.raises(ValueError):
        merge_event(MergePlan("A","B","same identity",()))

def test_merge_is_non_destructive_event():
    event=merge_event(MergePlan("A","B","same identity",("E1",)))
    assert event["event_type"]=="merge"
    assert event["entity_id"]=="A"
    assert event["target_entity_id"]=="B"
    assert "E1" in event["payload"]["evidence_ids"]

def test_self_merge_rejected():
    with pytest.raises(ValueError):
        merge_event(MergePlan("A","A","bad",("E1",)))
