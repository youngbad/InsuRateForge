from __future__ import annotations

from pydantic import BaseModel


class WhoAmIQuery(BaseModel):
    token: str
