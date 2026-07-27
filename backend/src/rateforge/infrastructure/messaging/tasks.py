from __future__ import annotations

import dramatiq

from rateforge.infrastructure.messaging.broker import broker


@dramatiq.actor(queue_name="notifications", broker=broker)
def send_notification(email: str, subject: str, message: str) -> dict[str, str]:
    return {"email": email, "subject": subject, "message": message, "status": "queued"}


@dramatiq.actor(queue_name="portfolio", broker=broker)
def run_portfolio_batch(run_id: str, quote_ids: list[str]) -> dict[str, object]:
    return {"run_id": run_id, "quote_ids": quote_ids, "status": "accepted"}
