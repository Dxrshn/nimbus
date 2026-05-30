import redis.asyncio as redis

from src.config import settings

_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(settings.redis_url, decode_responses=True)
    return _client


async def get_cached_url(short_code: str) -> str | None:
    client = get_redis()
    return await client.get(f"url:{short_code}")


async def set_cached_url(short_code: str, url: str, ttl: int = 3600) -> None:
    client = get_redis()
    await client.set(f"url:{short_code}", url, ex=ttl)


async def delete_cached_url(short_code: str) -> None:
    client = get_redis()
    await client.delete(f"url:{short_code}")


async def ping() -> bool:
    try:
        client = get_redis()
        return await client.ping()
    except Exception:
        return False