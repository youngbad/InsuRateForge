from __future__ import annotations

import pytest

MOTOR_PAYLOAD = {
    "driver_age": 34,
    "vehicle_value": 28000,
    "vehicle_type": "suv",
    "region": "urban",
    "annual_mileage": 16000,
    "cover_type": "comprehensive",
    "claims_last_5_years": 1,
    "no_claims_years": 4,
    "loyalty_years": 2,
    "additional_drivers": 1,
}


@pytest.mark.asyncio
async def test_pricing_preview_and_quote_creation(client) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "pricing@example.com",
            "full_name": "Pricing Customer",
            "password": "StrongPass123",
        },
    )
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "pricing@example.com", "password": "StrongPass123"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    preview_response = await client.post(
        "/api/v1/pricing/preview",
        json={"product_slug": "motor", "payload": MOTOR_PAYLOAD},
        headers=headers,
    )
    assert preview_response.status_code == 200
    preview = preview_response.json()
    assert preview["product_slug"] == "motor"
    assert preview["product_version"] == "2024.1"
    assert preview["base_premium"] >= 250
    assert preview["total_premium"] > preview["base_premium"] - preview["discounts_total"]
    assert preview["summary"]["product"] == "motor"

    quote_response = await client.post(
        "/api/v1/quotes/",
        json={"product_slug": "motor", "payload": MOTOR_PAYLOAD},
        headers=headers,
    )
    assert quote_response.status_code == 201
    quote = quote_response.json()
    assert quote["product_slug"] == "motor"
    assert quote["premium"] == preview["total_premium"]

    renew_response = await client.post(f"/api/v1/renewals/quotes/{quote['id']}", headers=headers)
    assert renew_response.status_code == 200
    renewed = renew_response.json()
    assert renewed["product_version"] == quote["product_version"]
    assert renewed["id"] != quote["id"]

    endorsement_response = await client.post(
        f"/api/v1/endorsements/quotes/{quote['id']}",
        json={"changes": {"annual_mileage": 22000, "additional_drivers": 2}},
        headers=headers,
    )
    assert endorsement_response.status_code == 200
    endorsed = endorsement_response.json()
    assert endorsed["premium"] >= quote["premium"]
