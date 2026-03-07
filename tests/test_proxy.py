import pytest

from knobs.cache import _cache
from knobs.proxy import KnobsProxy
from knobs.registry import Knob, _registry


@pytest.fixture(autouse=True)
def clean_registry():
    _registry.clear()
    _cache.update_all({})
    yield
    _registry.clear()
    _cache.update_all({})


def test_getattr_raises_for_undefined_knob():
    proxy = KnobsProxy()
    with pytest.raises(AttributeError, match="No config key 'MISSING' defined in KNOBS_CONFIG"):
        _ = proxy.MISSING


def test_getattr_returns_default_when_cache_empty():
    _registry["MY_KNOB"] = Knob(default=42)
    proxy = KnobsProxy()
    assert proxy.MY_KNOB == 42


def test_getattr_returns_cached_value():
    _registry["MY_KNOB"] = Knob(default=42)
    _cache.set("MY_KNOB", 99)
    proxy = KnobsProxy()
    assert proxy.MY_KNOB == 99


def test_dir_returns_registry_keys():
    _registry["A"] = Knob(default=1)
    _registry["B"] = Knob(default=2)
    proxy = KnobsProxy()
    assert sorted(dir(proxy)) == ["A", "B"]
