from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.application.auth.commands import AuthError, AuthService
from rateforge.application.auth.dtos import LoginDTO, RegisterUserDTO, TokenPairDTO, UserDTO
from rateforge.infrastructure.messaging.tasks import send_notification
from rateforge.presentation.dependencies import (
    get_auth_service,
    get_current_user,
    get_session,
    write_audit_log,
)

router = APIRouter()


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def register(
    command: RegisterUserDTO,
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_session),
) -> UserDTO:
    try:
        user = await auth_service.register(command)
        await write_audit_log(
            session,
            actor_user_id=user.id,
            action="user.registered",
            resource_type="user",
            resource_id=user.id,
            payload={"email": user.email},
        )
        send_notification.send(user.email, "Welcome to InsuRateForge", "Your account is ready.")
        return user
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=TokenPairDTO)
async def login(
    command: LoginDTO,
    auth_service: AuthService = Depends(get_auth_service),
    session: AsyncSession = Depends(get_session),
) -> TokenPairDTO:
    try:
        tokens = await auth_service.authenticate(command)
        await write_audit_log(
            session,
            actor_user_id=tokens.user.id,
            action="auth.login",
            resource_type="user",
            resource_id=tokens.user.id,
            payload={"email": tokens.user.email},
        )
        return tokens
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/refresh", response_model=TokenPairDTO)
async def refresh(request: RefreshRequest, auth_service: AuthService = Depends(get_auth_service)) -> TokenPairDTO:
    try:
        return await auth_service.refresh(request.refresh_token)
    except AuthError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.get("/me", response_model=UserDTO)
async def me(current_user=Depends(get_current_user)) -> UserDTO:
    return UserDTO(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        roles=current_user.roles,
        is_active=current_user.is_active,
    )
