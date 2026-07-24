from __future__ import annotations

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

REQUEST_COUNT = Counter(
    "rateforge_http_requests_total",
    "HTTP request count",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "rateforge_http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path"],
)
PRICING_COUNTER = Counter(
    "rateforge_pricing_requests_total",
    "Number of pricing operations",
    ["product_slug"],
)


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
