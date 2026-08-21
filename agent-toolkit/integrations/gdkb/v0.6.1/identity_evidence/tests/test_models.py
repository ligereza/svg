from app.model import Entity, Observation, Evidence, Assertion

def test_models_keep_identity_separate_from_observation():
    e=Entity("E1","substance","Example")
    o=Observation("O1","S1","R1",{"name":"Example"},"hash")
    assert e.id != o.id

def test_assertion_has_evidence_links():
    a=Assertion("A1","E1","related_to","E2",evidence_ids=("EV1",))
    assert a.evidence_ids == ("EV1",)
