from um import count

def test_basic():
    assert count("um") == 1
    assert count("um um um") == 3

def test_case_insensitive():
    assert count("Um") == 1
    assert count("UM um Um") == 3

def test_not_substring():
    assert count("yummy") == 0
    assert count("album") == 0
    assert count("instrument") == 0

def test_sentence():
    assert count("Hello, um, how are you?") == 1