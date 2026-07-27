from __future__ import annotations

import os

import dramatiq
from dramatiq.brokers.stub import StubBroker

_broker = None


def configure_broker(rabbitmq_url: str | None = None, testing: bool = False):  # type: ignore[no-untyped-def]
    global _broker
    if _broker is not None:
        return _broker
    url = rabbitmq_url or os.getenv("RATEFORGE_RABBITMQ_URL")
    if testing or not url:
        _broker = StubBroker()
    else:
        from dramatiq.brokers.rabbitmq import RabbitmqBroker

        _broker = RabbitmqBroker(url=url)
    dramatiq.set_broker(_broker)
    return _broker


broker = configure_broker()
