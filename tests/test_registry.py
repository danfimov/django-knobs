import pytest

from knobs.registry import Knob


@pytest.mark.parametrize("default,raw,expected", [
    (True, "true", True),
    (True, "1", True),
    (True, "yes", True),
    (False, "false", False),
    (False, "0", False),
    (False, "no", False),
    (0, "42", 42),
    (0.0, "3.14", 3.14),
    ("", "hello", "hello"),
])
def test_coerce_scalar_types(default, raw, expected):
    knob = Knob(default=default)
    assert knob.coerce(raw) == expected


def test_coerce_list():
    knob = Knob(default=[])
    assert knob.coerce('["a", "b"]') == ["a", "b"]


def test_coerce_dict():
    knob = Knob(default={})
    assert knob.coerce('{"key": "value"}') == {"key": "value"}


def test_serialize_bool():
    knob = Knob(default=True)
    assert knob.serialize(True) == "true"
    assert knob.serialize(False) == "false"


def test_serialize_int():
    knob = Knob(default=0)
    assert knob.serialize(7) == "7"


def test_serialize_float():
    knob = Knob(default=0.0)
    assert knob.serialize(1.5) == "1.5"


def test_serialize_str():
    knob = Knob(default="")
    assert knob.serialize("hello") == "hello"


def test_serialize_list():
    knob = Knob(default=[])
    assert knob.serialize([1, 2]) == "[1, 2]"


def test_serialize_dict():
    knob = Knob(default={})
    result = knob.serialize({"a": 1})
    import json
    assert json.loads(result) == {"a": 1}


def test_knob_infers_type_from_default():
    assert Knob(default=True).type is bool
    assert Knob(default=0).type is int
    assert Knob(default=0.0).type is float
    assert Knob(default="").type is str
    assert Knob(default=[]).type is list
    assert Knob(default={}).type is dict
