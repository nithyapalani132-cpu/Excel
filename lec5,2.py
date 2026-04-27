from bank import value


def test_hello():
    assert value("hello") == 0
    assert value("Hello") == 0
    assert value("hello there") == 0


def test_h():
    assert value("hi") == 20
    assert value("hey") == 20


def test_other():
    assert value("good morning") == 100
    assert value("what's up") == 100