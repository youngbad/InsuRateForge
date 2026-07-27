from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from rateforge.application.users.commands import UserService
from rateforge.application.users.dtos import CreateUserDTO, UserViewDTO
from rateforge.presentation.dependencies import get_user_service, require_roles

router = APIRouter()


@router.get("/", response_model=list[UserViewDTO])
async def list_users(
    user_service: UserService = Depends(get_user_service),
    _=Depends(require_roles("admin", "underwriter")),
) -> list[UserViewDTO]:
    return await user_service.list()


@router.post("/", response_model=UserViewDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    command: CreateUserDTO,
    user_service: UserService = Depends(get_user_service),
    _=Depends(require_roles("admin")),
) -> UserViewDTO:
    return await user_service.create(command)


@router.get("/{user_id}", response_model=UserViewDTO)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
    _=Depends(require_roles("admin", "underwriter")),
) -> UserViewDTO:
    user = await user_service.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
