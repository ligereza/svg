from app.fixture_loader import load_jsonl

def test_pubchem_fixture():
    rows=load_jsonl("fixtures/pubchem_small.jsonl")
    assert len(rows)==3
    assert rows[1]["payload"]["normalized_name"]=="cocaine"

def test_wikidata_fixture():
    rows=load_jsonl("fixtures/wikidata_small.jsonl")
    assert len(rows)==2
    assert "aliases" in rows[0]["payload"]
