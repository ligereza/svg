from app.resolver import Candidate, resolve

def test_identifier_is_confirmed():
    r = resolve("X", [Candidate("E1","X","source",True,1.0,True)])
    assert r.decision == "confirmed"
    assert r.entity_id == "E1"

def test_fuzzy_never_auto_confirms():
    r = resolve("cocaina", [Candidate("E1","cocaine","source",False,0.98)])
    assert r.decision == "candidate"

def test_ambiguous_exact_name_goes_to_review():
    cs = [
      Candidate("E1","common-name","A",True,1.0),
      Candidate("E2","common-name","B",True,1.0)
    ]
    r = resolve("common-name", cs)
    assert r.decision == "needs_review"
