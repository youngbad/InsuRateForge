from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.presentation.dependencies import get_session, list_audit_logs, require_roles

router = APIRouter()


@router.get("/logs")
async def get_audit_logs(
    session: AsyncSession = Depends(get_session),
    _=Depends(require_roles("admin", "underwriter")),
) -> list[dict[str, object]]:
    logs = await list_audit_logs(session)
    return [
        {
            "id": log.id,
            "actor_user_id": log.actor_user_id,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "payload": log.payload,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]
