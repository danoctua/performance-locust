import time
import threading

_timestamps = {}
_cache = {}


def memorize(key, period):
    lock = threading.Lock()

    def _decoration_wrapper(func):
        def _caching_wrapper(*args, **kwargs):
            cache_key = key
            now = time.time()

            if _timestamps.get(cache_key, now) > now:
                return _cache[cache_key]
            with lock:
                if _timestamps.get(cache_key, now) > now:
                    return _cache[cache_key]
                ret = func(*args, **kwargs)
                _cache[cache_key] = ret
                _timestamps[cache_key] = now + period
                return ret

        return _caching_wrapper

    return _decoration_wrapper
