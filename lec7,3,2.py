import pytest
from working import convert

def test_valid_times():
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("10:30 PM to 8:00 AM") == "22:30 to 08:00"

def test_invalid_format():
    with pytest.raises(ValueError):
        convert("9AM - 5PM")

def test_invalid_minutes():
    with pytest.raises(ValueError):
        convert("9:60 AM to 5:00 PM")

def test_invalid_hours():
    with pytest.raises(ValueError):
        convert("13 AM to 5 PM")