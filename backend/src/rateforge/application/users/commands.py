from __future__ import annotations

from rateforge.application.auth.commands import AuthService
from rateforge.application.users.dtos import CreateUserDTO, UserViewDTO
from rateforge.infrastructure.database.repositories.users import SQLAlchemyUserRepository


class UserService:
    def __init__(self, user_repo: SQLAlchemyUserRepository, auth_service: AuthService) -> None:
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def create(self, command: CreateUserDTO) -> UserViewDTO:
        user = await self.auth_service.register(command, allow_privileged_roles=True)
        return UserViewDTO.model_validate(user.model_dump())

    async def list(self) -> list[UserViewDTO]:
        users = await self.user_repo.list()
        return [
            UserViewDTO(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                roles=user.roles,
                is_active=user.is_active,
            )
            for user in users
        ]

    async def get(self, user_id: str) -> UserViewDTO | None:
        user = await self.user_repo.get(user_id)
        if user is None:
            return None
        return UserViewDTO(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            roles=user.roles,
            is_active=user.is_active,
        )
