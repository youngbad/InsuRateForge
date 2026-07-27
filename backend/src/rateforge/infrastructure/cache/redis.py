from __future__ import annotations

import json

from redis.asyncio import Redis

from rateforge.config import Settings


class RedisCache:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client: Redis | None = None

    async def connect(self) -> None:
        if self.settings.testing:
            return
        self.client = Redis.from_url(self.settings.redis_url, encoding="utf-8", decode_responses=True)

    async def get_json(self, key: str) -> dict[str, object] | None:
        if self.client is None:
            return None
        value = await self.client.get(key)
        return json.loads(value) if value else None

    async def set_json(self, key: str, value: dict[str, object], ttl_seconds: int = 300) -> None:
        if self.client is None:
            return
        await self.client.set(key, json.dumps(value), ex=ttl_seconds)

    async def close(self) -> None:
        if self.client is not None:
            await self.client.aclose()
