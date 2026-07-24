from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from rateforge.application.quotes.commands import QuoteService
from rateforge.application.quotes.dtos import CreateQuoteDTO, QuoteDTO
from rateforge.infrastructure.messaging.tasks import send_notification
from rateforge.presentation.dependencies import (
    get_current_user,
    get_quote_service,
    get_session,
    write_audit_log,
)

router = APIRouter()


@router.post("/", response_model=QuoteDTO, status_code=status.HTTP_201_CREATED)
async def create_quote(
    command: CreateQuoteDTO,
    quote_service: QuoteService = Depends(get_quote_service),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user),
) -> QuoteDTO:
    quote = await quote_service.create(command, current_user)
    await write_audit_log(
        session,
        actor_user_id=current_user.id,
        action="quote.created",
        resource_type="quote",
        resource_id=quote.id,
        payload={"product_slug": quote.product_slug, "premium": quote.premium},
    )
    send_notification.send(current_user.email, "Quote created", f"Quote {quote.id} is ready.")
    return quote


@router.get("/", response_model=list[QuoteDTO])
async def list_quotes(
    quote_service: QuoteService = Depends(get_quote_service),
    current_user=Depends(get_current_user),
) -> list[QuoteDTO]:
    return await quote_service.list_by_user(current_user.id)


@router.get("/{quote_id}", response_model=QuoteDTO)
async def get_quote(
    quote_id: str,
    quote_service: QuoteService = Depends(get_quote_service),
    current_user=Depends(get_current_user),
) -> QuoteDTO:
    quote = await quote_service.get(quote_id)
    if quote is None or (quote.user_id != current_user.id and "admin" not in current_user.roles):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
    return quote
