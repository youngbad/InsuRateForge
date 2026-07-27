from __future__ import annotations

from typing import Protocol

from rateforge.domain.quotes.entities import Quote


class QuoteRepository(Protocol):
    async def add(self, entity: Quote) -> Quote: ...
    async def get(self, entity_id: str) -> Quote | None: ...
    async def list_by_user(self, user_id: str) -> list[Quote]: ...
