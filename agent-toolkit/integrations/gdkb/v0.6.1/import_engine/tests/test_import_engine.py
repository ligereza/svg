from app.import_engine import ImportRecord, normalize_record, payload_hash, import_records

def test_import_is_deterministic():
    r=ImportRecord("PubChem","CID:1","compound",{"name":"Cocaína","formula":"X"})
    a=normalize_record(r)
    b=normalize_record(r)
    assert a==b
    assert len(a["payload_hash"])==64

def test_name_normalization_is_derived():
    r=ImportRecord("X","1","entity",{"name":"  Cocaína  "})
    out=normalize_record(r)
    assert out["payload"]["name"]=="  Cocaína  "
    assert out["payload"]["normalized_name"]=="cocaina"

def test_batch_import():
    rs=[
      ImportRecord("X","1","entity",{"name":"Alpha"}),
      ImportRecord("X","2","entity",{"name":"Beta"})
    ]
    assert len(import_records(rs))==2

def test_validation():
    try:
        normalize_record(ImportRecord("","1","entity",{}))
        assert False
    except ValueError:
        assert True
