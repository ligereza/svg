from app.normalize import normalize_name

def test_unicode_and_case():
    assert normalize_name("Cocaína") == normalize_name("COCAINA")

def test_whitespace():
    assert normalize_name("  alpha   beta ") == "alpha beta"
