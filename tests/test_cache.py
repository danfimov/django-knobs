import threading

from knobs.cache import LocalCache


def test_get_returns_default_for_missing_key():
    cache = LocalCache()
    assert cache.get("missing", default=42) == 42


def test_set_and_get():
    cache = LocalCache()
    cache.set("x", 99)
    assert cache.get("x") == 99


def test_update_all_replaces_data():
    cache = LocalCache()
    cache.set("old", 1)
    cache.update_all({"new": 2})
    assert cache.get("new") == 2
    assert cache.get("old") is None


def test_keys():
    cache = LocalCache()
    cache.update_all({"a": 1, "b": 2})
    assert sorted(cache.keys()) == ["a", "b"]


def test_thread_safe_concurrent_writes():
    cache = LocalCache()
    errors = []

    def writer(i):
        try:
            for _ in range(100):
                cache.set(f"key_{i}", i)
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=writer, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors


def test_thread_safe_concurrent_reads_and_writes():
    cache = LocalCache()
    cache.update_all({"k": 0})
    errors = []

    def reader():
        try:
            for _ in range(200):
                cache.get("k", 0)
        except Exception as e:
            errors.append(e)

    def writer():
        try:
            for i in range(200):
                cache.update_all({"k": i})
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=reader) for _ in range(5)]
    threads += [threading.Thread(target=writer) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
