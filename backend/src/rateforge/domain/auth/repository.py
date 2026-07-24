from __future__ import annotations

from typing import Protocol

from rateforge.domain.users.entities import User


class AuthRepository(Protocol):
    async def get_by_email(self, email: str) -> User | None: ...
    async def get(self, entity_id: str) -> User | None: ...
