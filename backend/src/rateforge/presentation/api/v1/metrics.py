from fastapi import APIRouter

from rateforge.infrastructure.observability.metrics import metrics_response

router = APIRouter()


@router.get("", include_in_schema=False)
async def get_metrics():  # type: ignore[no-untyped-def]
    return metrics_response()
