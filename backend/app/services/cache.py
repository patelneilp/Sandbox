from cachetools import TTLCache

from app.core.config import settings


class APICache:
    def __init__(self) -> None:
        self._cache = TTLCache(maxsize=10000, ttl=settings.cache_ttl_seconds)

    def get(self, key: str):
        return self._cache.get(key)

    def set(self, key: str, value):
        self._cache[key] = value


api_cache = APICache()
