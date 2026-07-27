from __future__ import annotations

from typing import Protocol, TypeVar

EntityT = TypeVar("EntityT")


class Repository(Protocol[EntityT]):
    async def add(self, entity: EntityT) -> EntityT: ...
    async def get(self, entity_id: str) -> EntityT | None: ...
