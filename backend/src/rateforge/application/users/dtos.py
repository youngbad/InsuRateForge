from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class CreateUserDTO(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2)
    password: str = Field(min_length=8)
    roles: list[str] = Field(default_factory=lambda: ["customer"])


class UserViewDTO(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    roles: list[str]
    is_active: bool
