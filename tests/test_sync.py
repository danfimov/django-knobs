import pytest

from knobs.cache import LocalCache
from knobs.registry import Knob


@pytest.fixture
def registry():
    return {
        "MAX_RETRIES": Knob(default=3, help_text="Max retries", category="reliability"),
        "DARK_MODE": Knob(default=False, help_text="Dark mode", category="ui"),
    }


@pytest.fixture
def cache():
    return LocalCache()


@pytest.mark.django_db
def test_sync_loads_db_values(registry, cache):
    from knobs.models import KnobValue
    from knobs.sync import SyncThread

    KnobValue.objects.create(name="MAX_RETRIES", raw_value="10")

    thread = SyncThread(interval=60, cache=cache, registry=registry)
    thread._sync()

    assert cache.get("MAX_RETRIES") == 10
    assert not cache.get("DARK_MODE")  # not in DB, uses default


@pytest.mark.django_db
def test_sync_detects_change(registry, cache):
    from knobs.models import KnobValue
    from knobs.sync import SyncThread

    kv = KnobValue.objects.create(name="MAX_RETRIES", raw_value="5")

    thread = SyncThread(interval=60, cache=cache, registry=registry)
    thread._sync()
    assert cache.get("MAX_RETRIES") == 5

    # Simulate an update by a different process
    kv.raw_value = "20"
    kv.save()

    thread._sync()
    assert cache.get("MAX_RETRIES") == 20


@pytest.mark.django_db
def test_sync_no_reload_when_unchanged(registry, cache, mocker):
    from knobs.models import KnobValue
    from knobs.sync import SyncThread

    KnobValue.objects.create(name="MAX_RETRIES", raw_value="7")
    KnobValue.objects.create(name="DARK_MODE", raw_value="false")

    thread = SyncThread(interval=60, cache=cache, registry=registry)
    thread._sync()

    reload_spy = mocker.spy(thread, "_reload_all")
    thread._sync()  # no changes — should not reload

    reload_spy.assert_not_called()


@pytest.mark.django_db
def test_post_save_signal_updates_cache():

    from knobs.cache import _cache
    from knobs.models import KnobValue
    from knobs.registry import _registry

    _registry.clear()
    _registry["MY_FLAG"] = Knob(default=False)
    _cache.set("MY_FLAG", False)

    try:
        KnobValue.objects.create(name="MY_FLAG", raw_value="true")
        assert _cache.get("MY_FLAG") is True
    finally:
        _registry.clear()
        _cache.update_all({})
        KnobValue.objects.filter(name="MY_FLAG").delete()
