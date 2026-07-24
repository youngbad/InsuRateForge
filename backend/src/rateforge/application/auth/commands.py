from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from rateforge.application.auth.dtos import LoginDTO, RegisterUserDTO, TokenPairDTO, UserDTO
from rateforge.config import Settings
from rateforge.domain.users.entities import User, UserRole
from rateforge.infrastructure.database.repositories.auth import SQLAlchemyAuthRepository
from rateforge.infrastructure.database.repositories.users import SQLAlchemyUserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthError(ValueError):
    pass


class AuthService:
    def __init__(
        self,
        settings: Settings,
        user_repo: SQLAlchemyUserRepository,
        auth_repo: SQLAlchemyAuthRepository,
    ) -> None:
        self.settings = settings
        self.user_repo = user_repo
        self.auth_repo = auth_repo

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _encode(self, subject: str, roles: list[str], token_type: str, ttl_minutes: int) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": subject,
            "roles": roles,
            "type": token_type,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=ttl_minutes)).timestamp()),
            "jti": str(uuid4()),
        }
        return jwt.encode(payload, self.settings.secret_key, algorithm=self.settings.jwt_algorithm)

    def decode_token(self, token: str, expected_type: str = "access") -> dict[str, object]:
        try:
            payload = jwt.decode(token, self.settings.secret_key, algorithms=[self.settings.jwt_algorithm])
        except JWTError as exc:
            raise AuthError("Invalid token") from exc
        if payload.get("type") != expected_type:
            raise AuthError(f"Expected {expected_type} token")
        return payload

    async def register(self, command: RegisterUserDTO, *, allow_privileged_roles: bool = False) -> UserDTO:
        existing = await self.auth_repo.get_by_email(command.email)
        if existing is not None:
            raise AuthError("User with this email already exists")
        roles = command.roles if allow_privileged_roles and command.roles else [UserRole.CUSTOMER.value]
        user = User(
            email=command.email,
            full_name=command.full_name,
            hashed_password=self.hash_password(command.password),
            roles=roles,
        )
        created = await self.user_repo.add(user)
        return self._to_dto(created)

    async def authenticate(self, command: LoginDTO) -> TokenPairDTO:
        user = await self.auth_repo.get_by_email(command.email)
        if user is None or not self.verify_password(command.password, user.hashed_password):
            raise AuthError("Invalid credentials")
        if not user.is_active:
            raise AuthError("User is inactive")
        return TokenPairDTO(
            access_token=self._encode(user.id, user.roles, "access", self.settings.access_token_ttl_minutes),
            refresh_token=self._encode(user.id, user.roles, "refresh", self.settings.refresh_token_ttl_minutes),
            user=self._to_dto(user),
        )

    async def refresh(self, refresh_token: str) -> TokenPairDTO:
        payload = self.decode_token(refresh_token, expected_type="refresh")
        subject = str(payload["sub"])
        user = await self.auth_repo.get(subject)
        if user is None:
            raise AuthError("User not found")
        return TokenPairDTO(
            access_token=self._encode(user.id, user.roles, "access", self.settings.access_token_ttl_minutes),
            refresh_token=self._encode(user.id, user.roles, "refresh", self.settings.refresh_token_ttl_minutes),
            user=self._to_dto(user),
        )

    async def get_current_user(self, token: str) -> User:
        payload = self.decode_token(token, expected_type="access")
        subject = str(payload["sub"])
        user = await self.auth_repo.get(subject)
        if user is None or not user.is_active:
            raise AuthError("Active user not found")
        return user

    @staticmethod
    def _to_dto(user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            roles=user.roles,
            is_active=user.is_active,
        )
